from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request,'projects/projects.html',context) #appname/htmlpage

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    return render(request,'projects/single-project.html',{'project':projectObj})

def createProject(request):
    form = ProjectForm() # create an instance of ProjectForm()

    if request.method == 'POST':
        print(request.POST)
        form = ProjectForm(request.POST,request.FILES) # reuqest.FILES process image in backend                                                                                        
        if form.is_valid():
            form.save()
            return redirect('projects')

    context={'form':form}
    return render(request, "projects/project_form.html" ,context)

def updateProject(request,pk):
    project = Project.objects.get(id=pk) # get the project where ID = Pk
    form = ProjectForm(instance=project) # create an instance of ProjectForm() and pass in the project ID

    if request.method == 'POST':
        print(request.POST)
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context={'form':form}
    return render(request, "projects/project_form.html" ,context)


def deleteProject(request,pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context={'object':project}
    return render(request,'projects/delete_template.html',context)