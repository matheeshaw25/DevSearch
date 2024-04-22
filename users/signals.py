from django.db.models.signals import post_save, post_delete #trigger anytime a model is saved.
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

#CONNECTED USING READY() METHOD IN APPS.PY


# Everytime a user is created, a user profile will be created automatically
# create profile signal
# @receiver(post_save, sender= Profile) 
def createProfile(sender,instance,created,**kwargs): #sender is model that is gonna send this | created lets us know if a new record in DB is added or not
    print('Profile Signal Triggered')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
 
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False: # we do not want this to be the first instance of the profile so thats why created should be equal to false
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()



#delete profile signal -> delete user too
def deleteUser(sender, instance, **kwargs): # delete user
    user = instance.user # instance here is the profile
    user.delete()
    print('Deleting user...')


post_save.connect(createProfile, sender=User)   
post_save.connect(updateUser, sender=Profile) # profile will send it
post_delete.connect(deleteUser, sender=Profile) 
