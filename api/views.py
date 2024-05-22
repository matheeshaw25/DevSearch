from rest_framework.decorators import api_view, permission_classes # something like @login_rerquired but for the Django Rest framework
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer # inmporting serializer
from projects.models import Project, Review, Tag

# from api import serializers

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

@api_view(['POST'])
@permission_classes([IsAuthenticated]) #user has to be authenticated. Like @login_required but for django rest framework
def projectVote(request,pk):
    project = Project.objects.get(id=pk) #1 get the project that we are working on
    user = request.user.profile #2 get the user profile (now we are getting the user from the token and not from the session because of @api_view decorator)
    data = request.data #3 get the data

    #5
    #get_or_create checks if there is a review with that user for that project in DB, then it will get that user, if that user doesnt exist then it will create that review for us
    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
        
    )
    review.value = data['value'] #6 getting the value and setting it
    review.save() #7 updating it
    project.getVoteCount #8 get the vote count

    serializer = ProjectSerializer(project, many=False)#4 make a serializer , (project we are going to serialize, many=false because we are getting a single instance of a project)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag'] #get the tagId
    projectId = request.data['project'] # get the projectId

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag) #remove this specific tag from the project

    return Response('Tag was deleted!')