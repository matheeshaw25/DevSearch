from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage


def paginateProfiles(request, profiles, results):

    page = request.GET.get('page') #page number
    paginator = Paginator(profiles, results) #pass into paginator function

    try:
        profiles = paginator.page(page) # set the projects to display paginator page number
    except PageNotAnInteger: # if page is not an integer
        page = 1
        profiles = paginator.page(page)
    except EmptyPage: # if page number is greater than maximum page number
        page = paginator.num_pages # get the maximum page number
        profiles = paginator.page(page) # pass it to the projects

    leftIndex = (int(page)-4) # left side value
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page)+5)   # right side value   
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex,rightIndex)

    return custom_range, profiles


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'): #getting the Search value
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains= search_query)
    #distinct() makes sure we only get one instance of each user
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in =skills)) #all profiles that contains search_query name or short intro

    return profiles , search_query
