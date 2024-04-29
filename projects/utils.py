from .models import Project , Tag
from django.db.models import Q
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage


def paginateProjects(request, projects, results):

    page = request.GET.get('page') #page number
   
    paginator = Paginator(projects, results) #pass into paginator function

    try:
        projects = paginator.page(page) # set the projects to display paginator page number
    except PageNotAnInteger: # if page is not an integer
        page = 1
        projects = paginator.page(page)
    except EmptyPage: # if page number is greater than maximum page number
        page = paginator.num_pages # get the maximum page number
        projects = paginator.page(page) # pass it to the projects

    leftIndex = (int(page)-4) # left side value
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page)+5)   # right side value   
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex,rightIndex)

    return custom_range, projects



def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'): #getting the Search value
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)    
    
    projects = Project.objects.distinct().filter(Q(title__icontains = search_query) | Q(description__icontains = search_query)|Q(owner__name__icontains = search_query) | Q(tags__in = tags)) #into parent owner-->into attribute bane
    return projects , search_query