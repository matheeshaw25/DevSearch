from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank = True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg") # profile picture and default image , also pip install pillow
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True , blank=True)
    tags = models.ManyToManyField('Tag',blank=True) # tag in quotes because the Tag model is below, if its above no need quotes
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): #converts an object method to a string   
        return self.title
        

class Review(models.Model):
    VOTE_TYPE = (
        ('up','Up Vote'),
        ('down','Down Vote'),       
    )
    #owner =   
    project = models.ForeignKey(Project, on_delete=models.CASCADE) #cascade removes all the reviews if project is deletedw
    body = models.TextField(null=True, blank = True)
    value = models.CharField(max_length=200,choices=VOTE_TYPE) 
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) :
        return self.value
    


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self) :
        return self.name