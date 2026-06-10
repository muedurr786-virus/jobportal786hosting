from django.urls import path
from .views import *

urlpatterns = [
    # Authentication URLs
    path('register/', register_page, name='register'),
    path('', loginpage, name='login'),
    path('logout/', logoutpage, name='logout'),
    
    # Core Dashboard
    path('dashboard/', dashboardpage, name='dashboard'),
    
    # Profile Setup URLs
    path('recruiter/', recuiterpage, name='recruiter'),
    path('jobseeker/', jobseekerpage, name='jobseeker'),
    
    # Job Posting & Skills Management
    path('job_post/', jobpostpage, name='job_post'),
    path('add_skill/', skillpage, name='add_skill'),
    path('skill_match/', skillmathingpage, name='skill_match'),
    
    # Application Dashboard Lists
    path('applications/', applicationpage, name='applicationlist'),       # Recruiter view
    path('my-applications/', myapplicationpage, name='my_applications'),   # Job seeker view
    
    # Application Management Actions (Status Updates)
    path('pending/<int:id>/', pendingpage, name='pending'),
    path('shortlist/<int:id>/', Shorlistgpage, name='shortlist'),
    path('reject/<int:id>/', Rejectgpage, name='reject'),
    path('apply_job/<int:id>/', applyJobPage, name='apply_job')
]

