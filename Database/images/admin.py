from django.contrib import admin
from .models import ImageModel ,Subscription  ,Membership,UserMembership ,ImageCategory ,VideoCategory ,VideoModel
from rozarpay.models import Transaction
# Register your models here. 
admin.site.register(ImageCategory)
admin.site.register(ImageModel)
# admin.site.register(Subscription)
class SubscriptionAdminModel(admin.ModelAdmin):
     list_display = ('user_membership', 'expires_in', 'active')
admin.site.register(Subscription,SubscriptionAdminModel)


# admin.site.register(Membership)

class MembershipAdminModel(admin.ModelAdmin):
     list_display = ('membership_type', 'duration', 'price')
admin.site.register(Membership,MembershipAdminModel)

# admin.site.register(UserMembership)





# admin.site.register(Transaction)
class TransactionAdminModel(admin.ModelAdmin):
     list_display = ('username', 'email', 'membership_type', 'amount', 'created_at', 'id')
admin.site.register(Transaction,TransactionAdminModel)

class TransactionItem(admin.TabularInline):

     model = Transaction

class UserMembershipAdminModel(admin.ModelAdmin):
    
     list_display = ('user', 'membership')
admin.site.register(UserMembership,UserMembershipAdminModel)



# admin.site.register(Test)
# class TestAdminModel(admin.StackedInline):
     
#      list_display = ('type', 'dur', 'period')

admin.site.register(VideoModel)



     
class VideoCategoryAdminModel(admin.ModelAdmin):
  
     list_display = ('video_category', 'name')
    
admin.site.register(VideoCategory)




