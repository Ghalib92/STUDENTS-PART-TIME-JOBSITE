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
