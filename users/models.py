from django.db import models
from django.contrib.auth.models import User # importing user model for one to one relationship in class Profile
import uuid
# Create your models here.

from django.db.models.signals import post_save, post_delete #trigger anytime a model is saved.
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png") # upload it to the profiles folder under static
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube= models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): #converts an object method to a string   
        return str(self.username)
    

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)    
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): #converts an object method to a string   
        return str(self.name)
    

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True) # one profile can have many messages , on_delete was kept null to not delete messages from receipent when sender account gets deleted
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages") #related_name = messages is used to denote that profile model is connected to recipient by messages | if we didnt use that it wont let profile model to get added twice becuz sender also added
    name = models.CharField(max_length=200, null=True , blank=True)
    email = models.EmailField(max_length=200, null=True , blank=True)
    subject = models.CharField(max_length=200, null=True , blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True) #read or undread
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): #converts an object method to a string   
        return self.subject
    
    class Meta:
        ordering = ['is_read','-created'] # - created means newer created