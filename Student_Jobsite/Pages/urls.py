from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name = 'logout'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobseeker-dashboard/', views.employee_dashboard, name='employee_dashboard'),
# Employer
    path('post-job/', views.post_job, name='post_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('applications/<int:job_id>/', views.job_applications, name='job_applications'),
    path('application-status/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('application-send-email/<int:application_id>/', views.send_application_email, name='send_application_email'),

# Job Seeker
    path('jobs/', views.available_jobs, name='available_jobs'),
    path('jobs/apply/<int:job_id>/', views.apply_to_job, name='apply_to_job'),
    path('applications/', views.my_applications, name='my_applications'),

# Chat
    path('chat/', views.chat_list, name='chat_list'),
    path('room/<int:thread_id>/', views.chat_room, name='chat_room'),

#request pay
    path('initiate-job-payment/', views.initiate_job_payment, name='initiate_job_payment'),
    path('request-payment/', views.request_payment, name='request_payment'),
    path('pay-requests/', views.view_pay_requests, name='view_pay_requests'),
    path('handle-pay-request/<int:request_id>/<str:action>/', views.handle_pay_request, name='handle_pay_request'),



]





