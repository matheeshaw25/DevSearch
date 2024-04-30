from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL) # one to many
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
    
    class Meta:
        ordering = ['-vote_ratio','-vote_total', 'title'] #high ratio and high total will be sorted first

    @property
    def reviewers(self): #people who have reviewed for a project
        queryset = self.review_set.all().values_list('owner__id', flat = True)
        return queryset


    @property
    def getVoteCount(self): #calculating the vote total and vote ratio
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes)*100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
        

class Review(models.Model):
    VOTE_TYPE = (
        ('up','Up Vote'),
        ('down','Down Vote'),       
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) #cascade removes all the reviews if project is deletedw
    body = models.TextField(null=True, blank = True)
    value = models.CharField(max_length=200,choices=VOTE_TYPE) 
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner','project']] #one owner can give one review

    def __str__(self) :
        return self.value
    


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self) :
        return self.name