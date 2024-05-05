from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name', # changing first_name 's label to name
        } 

    def __init__(self,*args,**kwargs):
            super(CustomUserCreationForm,self).__init__(*args,**kwargs)

            for name,field in self.fields.items():
                 field.widget.attrs.update({'class':'input'}) #setting an input class in the form    


class ProfileForm(ModelForm):
     class Meta:
          model = Profile
          fields = ['name', 'email', 'username' , 'location', 'bio' , 'short_intro', 'profile_image','social_github','social_linkedin'
                    ,'social_twitter','social_youtube','social_website']

    # styling textboxes as in CSS
     def __init__(self,*args,**kwargs):
            super(ProfileForm,self).__init__(*args,**kwargs)

            for name,field in self.fields.items():
                 field.widget.attrs.update({'class':'input'}) #setting an input class in the form  


class SkillForm(ModelForm): #create skill form
     class Meta:
          model = Skill #model your working with
          fields= '__all__' # show all the fields
          exclude = ['owner'] # except owner

         # styling textboxes as in CSS
     def __init__(self,*args,**kwargs):
            super(SkillForm,self).__init__(*args,**kwargs)

            for name,field in self.fields.items():
                 field.widget.attrs.update({'class':'input'}) #setting an input class in the form      


class MessageForm(ModelForm):
     class Meta:
          model = Message
          fields = ['name', 'email', 'subject', 'body']    

     def __init__(self,*args,**kwargs):
            super(MessageForm,self).__init__(*args,**kwargs)

            for name,field in self.fields.items():
                 field.widget.attrs.update({'class':'input'}) #setting an input class in the form                    