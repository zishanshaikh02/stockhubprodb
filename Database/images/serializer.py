from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
from .models import Membership




class ImageModelSerializer(ModelSerializer):

   
    class Meta:
        model = ImageModel
        fields = "__all__"  # Use double underscores to include all fields

class ImageCategorySerializer(ModelSerializer):
    image_cat =  ImageModelSerializer(many = True)

    

    class Meta:
        model = ImageCategory
        fields = "__all__"







############VIDEO SERIALIZER




class VideoModelSerializer(ModelSerializer):

   
    class Meta:
        model = VideoModel
        fields = "__all__"  # Use double underscores to include all fields

class VideoCategorySerializer(ModelSerializer):
    video_cat =  VideoModelSerializer(many = True)

    

    class Meta:
        model = VideoCategory
        fields = "__all__"






class SubscriptionsSerailizer(ModelSerializer):

    class Meta :
        model = Subscription
        fields = "__all__" 


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

