from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from .models import Profile , Skill , Message
from .forms import CustomUserCreationForm, ProfileForm ,  SkillForm , MessageForm
from .utils import searchProfiles , paginateProfiles
# Create your views here.


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated: #if i access login page after authentication , redirected to profiles
        return redirect('profiles')


    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username) #checks if username exist
        except:
            messages.error(request,'Username does not exist')    

        user = authenticate(request, username=username, password=password) # makes sure password matches username and returns that specific user

        if user is not None:
            login(request, user) # login function creates a session for the user in the DB and gets that session and adds it to browser cookies
            return redirect(request.GET['next']if 'next' in request.GET else 'account')
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
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range':custom_range}
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

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill was deleted successfully!')
        return redirect('account')
    context = {'object':skill} # we named it as object because we take the input as object in the delete_template.html page
    return render(request, 'delete_template.html', context)

# messages page
@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile # getting the currently logged in user
    messageRequests = profile.messages.all() # we renamed messages in "recepient" so thats why we dont use message_set.all()
    unreadCount = messageRequests.filter(is_read = False).count() #number of unread messages
    context ={'messageRequests':messageRequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html',context)

# read a message
@login_required(login_url='login')
def viewMessage(request,pk):
    profile =  request.user.profile # getting the current user
    message = profile.messages.get(id=pk) # message is the related_name in the model
    # MESSAGE READ AND UNREAD updating on template
    if message.is_read == False:  # if message is not read and
        message.is_read = True # now if message is read
        message.save() #save it as message was read
    context = {'message':message}
    return render(request, 'users/message.html', context)


def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    # checking if there is a sender or not
    try:
        sender = request.user.profile # if user logged in
    except:
        sender = None # if user not logged in

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)    
            message.sender = sender #either logged in user or none will be returned
            message.recipient = recipient

            # manually capturing the name and email of a person who is not logged in
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')    
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient':recipient,'form':form}
    return render(request, 'users/message_form.html', context)
