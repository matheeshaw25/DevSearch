from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm ,  SkillForm
# Create your views here.


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated: #if i access login page after authentication , redirected to profiles
        return redirect('profiles')


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username) #checks if username exist
        except:
            messages.error(request,'Username does not exist')    

        user = authenticate(request, username=username, password=password) # makes sure password matches username and returns that specific user

        if user is not None:
            login(request, user) # login function creates a session for the user in the DB and gets that session and adds it to browser cookies
            return redirect('profiles')
        else:
            messages.error(request,'Username OR Password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request,'User was logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #create a user object but hold the user before processing it
            user.username = user.username.lower()
            user.save()

            messages.success(request,'User account was created!')

            login(request,user)
            return redirect('edit-account')
        
        else:
            messages.success(request,'An error has occurred during registration')

    context={'page': page, 'form': form}
    return render(request, 'users/login_register.html',context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html',context)


def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="") # filters skills with no description
    otherSkills = profile.skill_set.filter(description="") # give skills with empty description



    context={'profile': profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile # getting the logged in user by using request.user

    skills = profile.skill_set.all()
    projects = profile.project_set.all()


    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile  = request.user.profile
    form = ProfileForm(instance=profile) #pre fill the fields with user information


    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance= profile) # request.FILES to pass the image
        if form.is_valid():
            form.save()

            return redirect('account')
        
    context={'form':form}
    return render(request, 'users/profile_form.html',context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill =  form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill was added successfully!')
            return redirect('account')

    context={'form':form}
    return render(request, 'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk) # will ensure only the owner can edit the skill
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill was updated successfully!')
            return redirect('account')

    context={'form':form}
    return render(request, 'users/skill_form.html',context)


def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill was deleted successfully!')
        return redirect('account')
    context = {'object':skill} # we named it as object because we take the input as object in the delete_template.html page
    return render(request, 'delete_template.html', context)