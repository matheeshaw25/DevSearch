from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


# takes profile model and convert it into a json object
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# takes project model and convert it into a json object
class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False) #many is false because only one owner
    tags = TagSerializer(many=True) # many is true because there is multiple tags
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj): # we wrote this because Tags are not included in the Project model.(GOTO projects.py->models.py)
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data



