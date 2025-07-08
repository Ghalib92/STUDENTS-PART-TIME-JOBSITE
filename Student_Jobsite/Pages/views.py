from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django .contrib.auth.models import User, auth
from .forms import SignUpForm, LoginForm
from .models import CustomUser




def home(request):
    return render (request, 'index.html')
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.role == 'employer':
                    return redirect('employer_dashboard')
                elif user.role == 'jobseeker':
                    return redirect('employee_dashboard')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def logout(request):
    auth.logout(request)
    return redirect('home') 


def employer_dashboard(request):
    return render(request, 'employer_dashboard.html')

def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')



#job addition and viewing views

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('my_jobs')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})


@login_required
def my_jobs(request):
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'my_jobs.html', {'jobs': jobs})



@login_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'applications.html', {'applications': applications, 'job': job})



# views.py
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from .models import Thread


@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(JobApplication, id=application_id, job__employer=request.user)

    if status in ['approved', 'rejected']:
        application.status = status
        application.save()

        # Create a thread if approved and not already created
        if status == 'approved':
            Thread.objects.get_or_create(
                employer=request.user,
                jobseeker=application.applicant,
                job=application.job
            )

        return render(request, 'modal_send_email.html', {
            'application': application,
            'status': status,
        })

    return redirect('job_applications', job_id=application.job.id)

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobApplication

login_required
def send_application_email(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, id=application_id, job__employer=request.user)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        to_email = application.email or application.applicant.email
        from_email = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, from_email, [to_email], fail_silently=False)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
@login_required
def available_jobs(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            return redirect('my_applications')
    else:
        form = JobApplicationForm()
    return render(request, 'apply.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'my_applications.html', {'applications': applications})


#chat implementation
# chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Message
from django.contrib.auth.decorators import login_required

@login_required
def chat_list(request):
    user = request.user
    if user.role == 'employer':
        threads = Thread.objects.filter(employer=user)
        return render(request, 'employer_chat_list.html', {'threads': threads})
        
    else:
        threads = Thread.objects.filter(jobseeker=user)
        return render(request, 'seeker_chat_list.html', {'threads': threads})
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread, Message


def chat_room(request, thread_id):
    user = request.user
    thread = get_object_or_404(Thread, id=thread_id)
    
    # Identify the other user
    other_user = thread.jobseeker if user == thread.employer else thread.employer

    # Handle message send
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                thread=thread,
                sender=user,
                content=content,
                is_read=False  # Not read yet
            )
            return redirect('chat_room', thread_id=thread.id)

    # ✅ Mark all unread messages from the other user as read
    Message.objects.filter(
        thread=thread,
        sender=other_user,
        is_read=False
    ).update(is_read=True)

    messages = Message.objects.filter(thread=thread).order_by('timestamp')

    # Render based on role
    if user.role == 'employer':
        return render(request, 'employer_chat_room.html', {
            'thread': thread,
            'messages': messages,
            'other_user': other_user,
        })
    else:
        return render(request, 'staff_chat_room.html', {
            'thread': thread,
            'messages': messages,
            'other_user': other_user,
        })



import requests
import base64
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import PayRequest

CONSUMER_KEY = 'X4ZJXQJpGJeGP07Ob7YIOazg5ZERCSb40DUTADBKuv4yke5X'
CONSUMER_SECRET = 'mBLMOtyuLsNO2YK7GASCww1UAc0AUJMrjVLVn74f90ta6hpoQpCBq7vpACUWtvCx'
SHORTCODE = '174379'
PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
CALLBACK_URL = 'https://example.com/callback/'  # Not used now

def get_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    return r.json().get('access_token')

def lipa_na_mpesa(phone_number, amount):
    access_token = get_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "JobPosting",
        "TransactionDesc": "Job Posting Fee"
    }

    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        json=payload,
        headers=headers
    )
    return response.json()

@csrf_exempt
def initiate_job_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        if not phone or not amount:
            return JsonResponse({'error': 'Missing phone or amount'}, status=400)
        response = lipa_na_mpesa(phone, amount)
        return JsonResponse(response)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)


# views.py
 
@login_required
def request_payment(request):
    applications = JobApplication.objects.filter(applicant=request.user, status='approved')

    # Get job applications for which payment is already requested
    requested_ids = PayRequest.objects.filter(
        requester=request.user
    ).values_list('job_application_id', flat=True)

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        if application_id and int(application_id) not in requested_ids:
            application = get_object_or_404(JobApplication, id=application_id, applicant=request.user)
            PayRequest.objects.create(
                job_application=application,
                requester=request.user
            )
            return redirect('request_payment')

    return render(request, 'request_payment.html', {
        'applications': applications,
        'requested_application_ids': requested_ids,
    })

@login_required
def view_pay_requests(request):
    if request.user.role != 'employer':
        return redirect('home')

    # Get all requests for this employer's jobs
    pay_requests = PayRequest.objects.filter(
        job_application__job__employer=request.user
    ).select_related('job_application', 'requester')

    return render(request, 'pay_requests.html', {'requests': pay_requests})



@login_required
def handle_pay_request(request, request_id, action):
    pay_request = get_object_or_404(PayRequest, id=request_id, job_application__job__employer=request.user)

    if action == 'accept':
        pay_request.status = 'accepted'
        # OPTIONAL: logic to notify admin to release funds
        # You can simulate release by sending email or updating another field
    elif action == 'reject':
        pay_request.status = 'rejected'

    pay_request.save()
    messages.success(request, f"Payment request has been {pay_request.status}.")
    return redirect('view_pay_requests')

