from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import RazorpayOrderSerializer, TranscationModelSerializer
from .rozarapi.main import RazorpayClient
from images.models import  UserMembership, Subscription, Membership
from django.contrib.auth.models import User 

rz_client = RazorpayClient()
# print(rz_client)

class RazorpayOrderAPIView(APIView):
    """This API will create an order"""

    def post(self, request):
        # Deserialize the incoming order data using the RazorpayOrderSerializer
        razorpay_order_serializer = RazorpayOrderSerializer(data=request.data)
      

        if razorpay_order_serializer.is_valid():
           
            # Extract the validated data from the serializer
            validated_data = razorpay_order_serializer.validated_data
           
            try:
                order_response = rz_client.create_order(
                amount=validated_data.get("amount"),
                currency=validated_data.get("currency"),
                    
     
)
          


                response = {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "order created",
                    "data": order_response
                }
                # print(response)
                
                return Response(response, status=status.HTTP_201_CREATED)
                

            except Exception as e:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e)
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": razorpay_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        



from datetime import datetime, timedelta

class TransactionAPIView(APIView):
    """This API will complete the order and save the transaction"""

    def post(self, request):
        transaction_serializer = TranscationModelSerializer(data=request.data)
        if transaction_serializer.is_valid():
            membership_type = transaction_serializer.validated_data.get("membership_type")
            user = request.user  # Assuming you are using authentication

            try:
                membership = Membership.objects.get(membership_type=membership_type)
            except Membership.DoesNotExist:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"Membership type '{membership_type}' does not exist.",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Define the calculate_expiration_date function
            def calculate_expiration_date(membership_type):
                duration_units_in_days = {
                    'Days': 1,
                    'Week': 7,
                    'Months': 30,  # Assuming 30 days in a month for simplicity
                }
                duration_in_days = membership.duration * duration_units_in_days.get(membership.duration_period)
                current_date = datetime.now()
                expiration_date = current_date + timedelta(days=duration_in_days)
                return expiration_date

            # Check if the user already has an active subscription
            try:
                user_membership = UserMembership.objects.get(user=user)
                active_subscription = Subscription.objects.filter(user_membership=user_membership, active=True).first()
                if active_subscription:
                    # Update the existing subscription with the new membership type
                    active_subscription.expires_in = calculate_expiration_date(membership_type)
                    active_subscription.save()
                else:
                    # Create a new Subscription for the existing UserMembership
                    Subscription.objects.create(user_membership=user_membership, active=True, expires_in=calculate_expiration_date(membership_type))
            except UserMembership.DoesNotExist:
                # If the user doesn't have any UserMembership, create a new one
                user_membership = UserMembership.objects.create(user=user, membership=membership)
                # Create a Subscription for the new UserMembership
                Subscription.objects.create(user_membership=user_membership, active=True, expires_in=calculate_expiration_date(membership_type))

            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "Transaction created, UserMembership and Subscription created/updated."
            }
            transaction_serializer.save()
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Bad request",
                "error": transaction_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



