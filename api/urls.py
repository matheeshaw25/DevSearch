from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView, # generate token based on user
    TokenRefreshView, # generate a refresh token
)

urlpatterns = [

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #generates a token (this expires soon eg: in 5min)
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # willl have a long life span , this comes everything the previous token expires
    
    path('', views.getRoutes),
    path('projects/',views.getProjects), #many projects
    path('projects/<str:pk>/',views.getProject), # single project
]
