from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name = 'logout'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobseeker-dashboard/', views.employee_dashboard, name='employee_dashboard'),
]
