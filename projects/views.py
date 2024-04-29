from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Project , Tag
from .forms import ProjectForm
from .utils import searchProjects


def projects(request):

    projects, search_query = searchProjects(request)
    
    context = {'projects':projects, 'search_query':search_query}
    return render(request,'projects/projects.html',context) #appname/htmlpage

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    return render(request,'projects/single-project.html',{'project':projectObj})

@login_required(login_url="login") #decorator to prevent this  page access without authentication
def createProject(request):
    profile = request.user.profile
    form = ProjectForm() # create an instance of ProjectForm()

    if request.method == 'POST':
        print(request.POST)
        form = ProjectForm(request.POST,request.FILES) # reuqest.FILES process image in backend                                                                                        
        if form.is_valid():
            project = form.save(commit=False) # give us an instance of the current project
            project.owner = profile #one to many relationship
            project.save()
            return redirect('account')

    context={'form':form}
    return render(request, "projects/project_form.html" ,context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk) # only querying the specific users projects | get the project where ID = Pk
    form = ProjectForm(instance=project) # create an instance of ProjectForm() and pass in the project ID

    if request.method == 'POST':
        print(request.POST)
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context={'form':form}
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
