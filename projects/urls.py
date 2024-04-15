from django.urls import path
from .import views

urlpatterns=[
    path('',views.projects, name="projects"), #url route, execute function name
    path('project/<str:pk>/',views.project, name="project"),#project/1, views.py.project function, function name
    path('create-project/',views.createProject,name= "create-project"),
    path('update-project/<str:pk>/',views.updateProject, name="update-project"),

    path('delete-project/<str:pk>/',views.deleteProject, name="delete-project"),
]