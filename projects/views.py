from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project , Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects , paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)  #6 number of projects per page

    context = {'projects':projects, 'search_query':search_query,  'custom_range':custom_range}
    return render(request,'projects/projects.html',context) #appname/htmlpage

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project =  projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        #update project vote count
        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk= projectObj.id)

    context = {'project':projectObj,'form':form}
    return render(request,'projects/single-project.html',context)

@login_required(login_url="login") #decorator to prevent this  page access without authentication
def createProject(request):
    profile = request.user.profile
    form = ProjectForm() # create an instance of ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split() #get the tag and split each individual word by the spaces
        form = ProjectForm(request.POST,request.FILES) # reuqest.FILES process image in backend                                                                                        
        if form.is_valid():
            project = form.save(commit=False) # give us an instance of the current project
            project.owner = profile #one to many relationship
            project.save()
            #Adding tags
            for tag in newtags: # loop through the news tags
                tag, created = Tag.objects.get_or_create(name=tag) #create a tag if it doesnt already exist or if one exists qeury that value
                project.tags.add(tag) # add new tag to tags model DB

            return redirect('account')

    context={'form':form}
    return render(request, "projects/project_form.html" ,context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk) # only querying the specific users projects | get the project where ID = Pk
    form = ProjectForm(instance=project) # create an instance of ProjectForm() and pass in the project ID

    if request.method == 'POST':
        #Adding tags , getting DATA from html page
        newtags = request.POST.get('newtags').replace(',', " ").split() #get the tag and split each individual word by the spaces

        
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            project = form.save() # take the instance of the newly created project
            for tag in newtags: # loop through the news tags
                tag, created = Tag.objects.get_or_create(name=tag) #create a tag if it doesnt already exist or if one exists qeury that value
                project.tags.add(tag) # add new tag to tags model DB

            return redirect('account')

    context={'form':form,'project':project}
    return render(request, "projects/project_form.html" ,context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context={'object':project}
    return render(request,'delete_template.html',context) # just delete-template without proper url path because its in the root directory
