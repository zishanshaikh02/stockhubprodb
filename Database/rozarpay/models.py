
from django.db import models

class Transaction(models.Model):

    payment_id = models.CharField(max_length=200, verbose_name="Payment ID")
    order_id = models.CharField(max_length=200, verbose_name="Order ID")
    signature = models.CharField(max_length=500, verbose_name="Signature", blank=True, null=True)
    amount = models.IntegerField(verbose_name="Amount")
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField( max_length=100,blank=True)
    # id = models.IntegerField( required=False, allow_blank=True)
    membership_type = models.CharField(max_length=100, verbose_name="membership_type", blank=True, null=True)
    duration = models.CharField(max_length=100, verbose_name="duration", blank=True, null=True)
    duration_period = models.CharField(max_length=100, verbose_name="duration_period", blank=True, null=True)

    username = models.CharField(max_length=100, verbose_name="username", blank=True, null=True)
    email = models.CharField(max_length=100, verbose_name="email", blank=True, null=True)



    def __str__(self):
        return str(self.id)
