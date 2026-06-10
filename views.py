from django.shortcuts import render, redirect
from django.contrib.auth import login, logout  
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_page(req):
    if req.method == 'POST':
        form = UserCustForm(req.POST) 
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCustForm()
        
    con = {
        'form': form,
        'Form_titel': 'Register Page',
        'btn': 'Register'
    }
    return render(req, 'auth/baseForm.html', con)


def loginpage(req):
    if req.method == 'POST':
        form = AuthForm(req, data=req.POST)  
        if form.is_valid():
            user = form.get_user()
            login(req, user)  
            return redirect('dashboard')  
    else:
        form = AuthForm()
        
    con = {
        'form': form,
        'Form_titel': 'Login Page',  
        'btn': 'Login'               
    }
    return render(req, 'auth/baseForm.html', con)


def logoutpage(req):
    logout(req)
    return redirect('login')


def dashboardpage(req):

    job_list = JobPostModel.objects.all()
    con={
        'job': job_list
    }
    return render(req, 'dashboard.html',con)
    
@login_required
def recuiterpage(req):
    try:
        recruiter = RecuiterModel.objects.get(user=req.user)
    except RecuiterModel.DoesNotExist:
        recruiter = RecuiterModel.objects.create(user=req.user)
        
    if req.method == "POST":
        form = RecuiterForm(req.POST, req.FILES, instance=recruiter)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = RecuiterForm(instance=recruiter)
        
    con = {
        'form': form,
        'Form_titel': 'Recruiter Profile Page', 
        'btn': 'Update Profile'                 
    }
    return render(req, 'baseform.html', con)

@login_required
def jobseekerpage(req):
    try:
        seeker = JobSeekerModel.objects.get(user=req.user)
    except JobSeekerModel.DoesNotExist:
        seeker = JobSeekerModel.objects.create(user=req.user)
        
    if req.method == "POST":
        form = JobSeekerForm(req.POST, req.FILES, instance=seeker)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JobSeekerForm(instance=seeker)
        
    con = {
        'form': form,
        'Form_titel': 'Job Seeker Profile Page',  
        'btn': 'Update Profile'                 
    }
    return render(req, 'baseform.html', con)

@login_required
def jobpostpage(req):
    try:
        recruiter = RecuiterModel.objects.get(user=req.user)
    except RecuiterModel.DoesNotExist:
        recruiter = RecuiterModel.objects.create(user=req.user)
        
    if req.method == "POST":
        form = JobpostForm(req.POST, req.FILES) 
        if form.is_valid():
            data = form.save(commit=False)
            data.user = req.user  
            data.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = JobpostForm()
        
    con = {
        'form': form,
        'Form_titel': 'Create Job Post',  
        'btn': 'Post Job'                 
    }
    return render(req, 'baseform.html', con)

@login_required
def applyJobPage(request,id):
    
    job = JobPostModel.objects.get(id=id)
    try:
        applicant = JobSeekerModel.objects.get(user=request.user)
    except JobSeekerModel.DoesNotExist:
        messages.error(request,"Update your profile First")
        return redirect('jobseeker')


    if request.user.user_type == "JobSeeker":
        
        if applicant and job:
            AppliedModel.objects.create(
            job_post = applicant,
            job = job,
            status = 'Pending'
        )
        messages.success(request,"Successfully Applied")
        

    return redirect("dashboard")

@login_required
def skillpage(req):
    if req.method == "POST":
        form = SkillForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, 'Skill Added Successfully!')
            return redirect('dashboard')
    else:
        form = SkillForm()

    con = {
        'form': form,
        'Form_titel': 'Add New Skill',
        'btn': 'Add Skill'
    }
    return render(req, 'baseform.html', con)
@login_required
def skillmathingpage(req):
    user_jobs = JobPostModel.objects.filter(user=req.user)
    if not user_jobs.exists():
        return redirect('dashboard')
    user_skills = user_jobs.values_list('skill_set', flat=True).distinct()
    if user_skills and None not in user_skills:
        jobs = JobPostModel.objects.filter(skill_set__in=user_skills).exclude(user=req.user).distinct()
    else:
        jobs = JobPostModel.objects.none() 

    con = {
        'jobs': jobs,
    }

    return render(req,'skill_match.html',con)


@login_required
def applicationpage(req):
    try:
        ricuter = RecuiterModel.objects.get(user=req.user)
    except RecuiterModel.DoesNotExist:
        ricuter = RecuiterModel.objects.create(user=req.user)

    Apply = AppliedModel.objects.filter(job__user=req.user)

    con = {
        'Apply': Apply,
    }
    return render(req, 'list.html', con)

def myapplicationpage(req):
    try:
        seeker = JobSeekerModel.objects.get(user=req.user)
    except JobSeekerModel.DoesNotExist:
        seeker = JobSeekerModel.objects.create(user=req.user)

    myapplication = AppliedModel.objects.filter(job_post=seeker)

    con = {
        'myapplication': myapplication,
    }

    return render(req, 'my_list.html', con)

@login_required
def pendingpage(req,id):
    
    apply_id = AppliedModel.objects.get(id=id)
    apply_id.status = 'Pending'
    apply_id.save()

    return redirect('applicationlist')

@login_required
def Shorlistgpage(req,id):

    apply_id = AppliedModel.objects.get(id=id)
    apply_id.status = 'Shorlist'
    apply_id.save()

    return redirect('applicationlist')

@login_required
def Rejectgpage(req,id):

    apply_id = AppliedModel.objects.get(id=id)
    apply_id.status = 'Reject'
    apply_id.save()

    return redirect('applicationlist')

