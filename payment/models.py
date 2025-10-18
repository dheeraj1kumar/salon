
from django.db import models
from django.conf import settings
from booking.models import Booking 

class Payment(models.Model):
    GATEWAY_RAZORPAY = "razorpay"
    GATEWAYS = [
        ("razorpay", "Razorpay"),
    ]
    STATUS_CREATED = "created"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_REFUND_PENDING = "refund_pending"
    STATUS_REFUNDED = "refunded"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Created"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
        (STATUS_REFUND_PENDING, "Refund Pending"),
        (STATUS_REFUNDED, "Refunded"),
    ]

    order_id = models.CharField(max_length=100, unique=True)   
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=255, blank=True, null=True)
    gateway = models.CharField(max_length=20, choices=GATEWAYS, default="razorpay")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bookings = models.ManyToManyField(Booking, related_name="payments")  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    refund_id = models.CharField(max_length=255, blank=True, null=True)  
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"{self.order_id} - {self.status}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

   
        for booking in self.bookings.all():
            booking.is_paid = True
            booking.save(update_fields=["is_paid"])
