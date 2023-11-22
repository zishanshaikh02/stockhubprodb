from rest_framework import serializers
from .models import Transaction

class RazorpayOrderSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)  # Update to DecimalField if needed
    currency = serializers.CharField()

    username = serializers.CharField(max_length=100, required=False, allow_blank=True)
    id = serializers.CharField(max_length=100, required=False, allow_blank=True)
    membership_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    duration = serializers.CharField(max_length=100, required=False, allow_blank=True)
    duration_period = serializers.CharField(max_length=100, required=False, allow_blank=True)



class TranscationModelSerializer(serializers.ModelSerializer):
    # Define custom fields for the shipping address
    user = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    # full_name = serializers.CharField(source='shipping_address.full_name', required=False)
    # mobile_number = serializers.CharField(source='shipping_address.mobile_number', required=False)
    # street_address = serializers.CharField(source='shipping_address.street_address', required=False)
    # area = serializers.CharField(source='shipping_address.area', required=False)
    # landmark = serializers.CharField(source='shipping_address.landmark', required=False)
    # state = serializers.CharField(source='shipping_address.state', required=False)
    # city = serializers.CharField(source='shipping_address.city', required=False)
    # pin_code = serializers.CharField(source='shipping_address.pin_code', required=False)
    # country = serializers.CharField(source='shipping_address.country', required=False)
    
   


    class Meta:
        model = Transaction
        fields = "__all__"
