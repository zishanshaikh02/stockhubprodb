from . import client  # Import your Razorpay client module
from rest_framework.serializers import ValidationError
from rest_framework import status
print(client)

class RazorpayClient:

    def create_order(self, amount, currency):

        # Prepare the data for creating a Razorpay order, shipping_address, cartItems, username, email, itemsPrice, taxPrice, shippingPrice
        data = {
            "amount": int(amount * 100),  # Convert amount to the required format (e.g., cents)
            "currency": currency,
         

        }
        try:
            # Create the Razorpay order using the client
            self.order = client.order.create(data=data)
            # print(self.razorpay_order_id)
            # print(self.razorpay_payment_id)
            # print(self.razorpay_signature)

            return self.order
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e)
                }
            )
            
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            self.verify_signature = client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            return self.verify_signature
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": e
                }
            )
     