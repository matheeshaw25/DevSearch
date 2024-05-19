from rest_framework.decorators import api_view, permission_classes # something like @login_rerquired but for the Django Rest framework
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer # inmporting serializer
from projects.models import Project

from api import serializers

@api_view(['GET'])# using this decorator 
def getRoutes(request): #gets all the routes of urls and returns in JSON format

    routes=[
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'}, 
        {'POST':'/api/users/token/refresh'}, # when users token expries it keeps the user logged in job of 'refresh'
    ]

    return Response(routes) # return part

@api_view(['GET'])
def getProjects(request):
    print('USER:', request.user)
    projects = Project.objects.all() #get all the projects
    serializer = ProjectSerializer(projects, many= True) #get the projects and convert into JSON, many=True because we are serializing many objects
    return Response(serializer.data)

@api_view(['GET'])
def getProject (request,pk):
    project = Project.objects.get(id=pk) #get all the projects
    serializer = ProjectSerializer(project, many= False) #get the projects and convert into JSON, many=Falswe because we are serializing one object
    return Response(serializer.data)