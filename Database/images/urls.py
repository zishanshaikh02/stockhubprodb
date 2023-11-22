from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageModelViewSet, download_image,check_subscription_status,MembershipViewSet ,ImageCategoryViewset ,VideoCategoryViewset,ImageHomeViewSet, download_video


admin.site.site_header = "Admin Panel"
admin.site.site_title = "admin panel"
admin.site.index_title = "StockBoxPro Admin Panel"
router = DefaultRouter()
router.register(r'images', ImageModelViewSet, basename="image")
router.register(r'images-home', ImageHomeViewSet, basename="image")

router.register(r'images-cat',ImageCategoryViewset ,basename= "images-cat")
router.register(r'video-cat',VideoCategoryViewset,basename='video-cat')




urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),

    path('image-download/<int:image_id>', download_image),
    path('check-subscription-status/', check_subscription_status),
     path('video-download/<int:video_id>/', download_video, name='download_video'),
   

    path('memberships/', MembershipViewSet.as_view({'get': 'list', 'post': 'create'})),
     
]
