from django.db.models import Q
from .models import Profile, Skill


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'): #getting the Search value
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains= search_query)
    #distinct() makes sure we only get one instance of each user
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in =skills)) #all profiles that contains search_query name or short intro

    return profiles , search_query
