from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont
from django.db import models
from django.core.files import File

class ImageCategory(models.Model):
    category_name = models.CharField(max_length=255,primary_key=True)

    def __str__(self) -> str:
        return self.category_name


class ImageModel(models.Model):
    category =  models.ForeignKey(ImageCategory,on_delete=models.CASCADE,related_name='image_cat',null=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to ='imagesdata/')
    copy_img = models.ImageField(upload_to="copydata/" ,null=True)
    description = models.TextField()
    is_home_only = models.BooleanField(default=False)

    def add_watermark(self):
        image = Image.open(self.copy_img.path)
        draw = ImageDraw.Draw(image)
        # width, height = image.size
        width, height = 900,600
        
        watermark_text = "©StockBoxPro"
        # font = ImageFont.load_default()
        font_size = 86  # Adjust the font size as needed
        font = ImageFont.truetype("arial.ttf", font_size)

        text_width, text_height = draw.textsize(watermark_text, font)  # Use draw.textsize() to get text size
        x = (width - text_width) // 2
        y = (height - text_height) // 2


        draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)
        image.save(self.copy_img.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.add_watermark()


   
    def __str__(self) -> str:
        return self.name
    def is_downloadable(self, user):
        if user.is_authenticated:
            try:
                user_membership = user.user_membership
                if user_membership.membership and user_membership.membership.active:
                    return True
            except UserMembership.DoesNotExist:
                pass
        return False
    



################VIDEO#####################


class VideoCategory(models.Model):
    video_name = models.CharField(max_length=255,primary_key=True)

    def __str__(self) -> str:
        return self.video_name



class VideoModel(models.Model):
    video_category =  models.ForeignKey(VideoCategory,on_delete=models.CASCADE,related_name='video_cat',null=True)
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to ='videodata/')
    copy_video = models.FileField(upload_to ='copyvideodata/', null=True)
    description = models.TextField()
    is_home_only = models.BooleanField(default=False)



   
    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Week', 'Week'),
        ('Months', 'Months'),
    )
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField( max_length=255,verbose_name='Membership Type')
    duration = models.PositiveIntegerField(default=7,verbose_name='Duration')
    duration_period = models.CharField(max_length=100, default='Day', choices=PERIOD_DURATION,verbose_name='Duration Unit')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,verbose_name='Price')

    def __str__(self):
        return f'{self.membership_type} - {self.duration} {self.duration_period} Membership'
from api.models import User
#### User Membership
class UserMembership(models.Model):
    user = models.OneToOneField(User, related_name='user_membership', on_delete=models.CASCADE,verbose_name='username ')
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user.email} - {self.membership} '
 





class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.user_membership.user} - {self.active} Subscription'
    def is_active(self):
        if self.expires_in and self.expires_in < timezone.now().date():
            self.active = False
            self.save()
        return self.active





