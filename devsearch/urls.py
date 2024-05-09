from django.contrib import admin
from django.urls import path, include

from django.conf import settings #have access to sttings.py to connect media root and media url
from django.conf.urls.static import static # helps to create a url for static files

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/',include('projects.urls')), #go to projects folder --> go to urls.py file
    path('',include('users.urls')),

    #1
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "reset_password.html"),name="reset_password"), # render template and perform logic of sending email to the user
    #2
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "reset_password_sent.html"), name="password_reset_done"),
    #3
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "reset.html"), name="password_reset_confirm"),
    #4
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name ="reset_password_complete.html"), name="password_reset_complete"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #goto settings, grab the url and connect to media root
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #url path from static url to static root


# 1 - User submits email for reset              //PasswordResetView.as_view()           //name="reset_password"
# 2 - Email sent message                        //PasswordResetDoneView.as_view()        //name="passsword_reset_done"
# 3 - Email with link and reset instructions    //PasswordResetConfirmView()            //name="password_reset_confirm"
# 4 - Password successfully reset message       //PasswordResetCompleteView.as_view()   //name="password_reset_complete"

# class based views are like functions but are classes hence we use .as_view()