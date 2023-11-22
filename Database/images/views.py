from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.http import HttpResponse ,Http404 ,HttpResponseForbidden ,FileResponse
from django.shortcuts import get_object_or_404
from .models import ImageModel
from .models import Subscription
from datetime import datetime

# Create your views here.
from .serializer import *
from .models import *
import os


from django.utils import timezone
from images.models import Subscription



class SubscriptionsViewset(ModelViewSet):
  

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionsSerailizer
   


###############################


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # Set the number of items per page

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.num_pages,  # Count is the number of pages available
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
    


# from rest_framework import viewsets
# from .models import ImageModel
# from .serializer import ImageModelSerializer ,ImageCategorySerializer

# class ImageModelViewSet(viewsets.ModelViewSet):
#     queryset = ImageModel.objects.all()
#     serializer_class = ImageModelSerializer
#     pagination_class = CustomPageNumberPagination

   


from rest_framework import viewsets
from .models import ImageModel
from .serializer import ImageModelSerializer ,ImageCategorySerializer
from django.db.models import Q

from django.db.models import Q

class ImageModelViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('search_keyword', '')

        if keyword:
          
            # Use Q objects to filter based on category name and description
            return ImageModel.objects.filter(
                Q(category__category_name__icontains=keyword) | Q(description__icontains=keyword) | Q(name__icontains=keyword) 
            )
        else:
            return ImageModel.objects.all()
        

####################################Home 
class ImageHomeViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('search_keyword', '')
        print(keyword)

        if keyword:
          
            # Use Q objects to filter based on category name and description
            return ImageModel.objects.filter(
               Q(category__category_name__icontains=keyword) | Q(description__icontains=keyword) | Q(name__icontains=keyword) | Q(is_home_only=True) 
            )
        
        else:
            return ImageModel.objects.all()

       


#    | Q(is_home_only=True) 
# import requests

# ngrok_url = "https://colab.research.google.com/drive/19f1sqUjQ3_AbP35vfMRLEIDvpp1eCNsr#scrollTo=Dac3dT6a5Ym_"  # Replace with your ngrok URL
# response = requests.get(ngrok_url)
# print(response.text)

    



from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import ImageModel
from django.views.static import serve
from django.conf import settings



# ##############################

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import ImageModel
from .models import UserMembership
from .models import Subscription
import os

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_image(request, image_id):
    image = get_object_or_404(ImageModel, pk=image_id)
    
    user = request.user
    print(user)  # This contains user data from the JWT token, provided by Simple JWT.
    
    user_membership = UserMembership.objects.filter(user=user).first()
    print("member:", user_membership)
    
    # Check if the user has an active subscription
    if user_membership:
        subscription = Subscription.objects.filter(user_membership=user_membership, active=True).first()
        if subscription:
            # Get the path to the image file on your server
            image_path = image.image.path

            if os.path.exists(image_path):
                with open(image_path, 'rb') as image_file:
                    response = HttpResponse(image_file.read(), content_type='image/png')
                    response['Content-Disposition'] = f'attachment; filename="{image.name}.png"'
                    return response
            else:
                raise Http404("Image not found")
        else:
            return HttpResponse("You must have an active subscription to download this image.")
    else:
        return HttpResponse("You must have an active subscription to download this image.")
######################################

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserMembership
from .models import Subscription

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_subscription_status(request):
    user = request.user
    user_membership = UserMembership.objects.filter(user=user).first()
    
    if user_membership:
        subscription = Subscription.objects.filter(user_membership=user_membership, active=True).first()
        if subscription:
            return Response({"active": True})
    
    return Response({"active": False})


#################

from rest_framework import viewsets
from .models import Membership
from .serializer import MembershipSerializer

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer



class ImageCategoryViewset(viewsets.ModelViewSet):
    queryset =  ImageCategory.objects.all()
    serializer_class = ImageCategorySerializer


    def get_queryset(self):
        keyword = self.request.query_params.get('search_keyword', '')
        

        # Use icontains for case-insensitive search on the name field
        if keyword:
            
         
            return   ImageCategory.objects.filter(category_name__icontains=keyword  )

            
        else:
            return ImageCategory.objects.all()
        
#################VIDEO VIEWSET ################

class VideoCategoryViewset(viewsets.ModelViewSet):
    queryset =  VideoModel.objects.all()
    serializer_class = VideoModelSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('search_keyword', '')

        if keyword:
          
            # Use Q objects to filter based on category name and description
            return VideoModel.objects.filter(
                Q(video_category__video_name__icontains=keyword) | Q(description__icontains=keyword) | Q(name__icontains=keyword) 
            )
        else:
            return VideoModel.objects.all()


###################  video download

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import VideoModel
from .models import UserMembership
from .models import Subscription
import os

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_video(request, video_id):
    video = get_object_or_404(VideoModel, pk=video_id)
    
    user = request.user
    print(user)  # This contains user data from the JWT token, provided by Simple JWT.
    
    user_membership = UserMembership.objects.filter(user=user).first()
    print("member:", user_membership)
    
    # Check if the user has an active subscription
    if user_membership:
        subscription = Subscription.objects.filter(user_membership=user_membership, active=True).first()
        if subscription:
            # Get the path to the video file on your server
            video_path = video.video.path

            if os.path.exists(video_path):
                with open(video_path, 'rb') as video_file:
                    response = HttpResponse(video_file.read(), content_type='video/mp4')
                    response['Content-Disposition'] = f'attachment; filename="{video.name}.mp4"'
                    return response
            else:
                raise Http404("Video not found")
        else:
            return HttpResponse("You must have an active subscription to download this video.")
    else:
        return HttpResponse("You must have an active subscription to download this video.")




