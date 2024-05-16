from rest_framework import serializers
from projects.models import Project

# takes project model and convert it into a json object
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'