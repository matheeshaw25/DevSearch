from django.shortcuts import render
from .models import Profile
# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html',context)


def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="") # filters skills with no description
    otherSkills = profile.skill_set.filter(description="") # give skills with empty description



    context={'profile': profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)