from django.db import models
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta, time,datetime
from dashboard.models import Service  
from django.utils import timezone


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"










class Booking(models.Model):
    STATUS_UPCOMING = "upcoming"
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELED = "canceled"
    STATUS_REFUNDED = "refunded"

    PAYMENT_NONE = "Unpaid"
    PAYMENT_PAID = "paid"
    PAYMENT_REFUND_PENDING = "refund_pending"
    PAYMENT_REFUNDED = "refunded"
    PAYMENT_FAILED = "failed"


    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_NONE, "Unpaid"),
        (PAYMENT_PAID, "Paid"),
        (PAYMENT_REFUND_PENDING, "Refund Pending"),
        (PAYMENT_REFUNDED, "Refunded"),
        (PAYMENT_FAILED, "Failed"),
    ]

    STATUS_CHOICES = [
        (STATUS_UPCOMING, "Upcoming"),
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELED, "Canceled"),
        (STATUS_REFUNDED, "refunded")
    ]
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, editable=False)
    service = models.ForeignKey('dashboard.Service', on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.TimeField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_NONE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_UPCOMING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey('booking.Staff', null=True, blank=True, on_delete=models.SET_NULL, related_name='bookings')
    refund_id = models.CharField(max_length=255, blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        indexes = [models.Index(fields=['status', 'date'])]

    def __str__(self):
        return f"{self.user} - {self.service.name} on {self.date} at {self.slot} [{self.status}]"

    def scheduled_datetime(self):
        
        naive = datetime.combine(self.date, self.slot)
        return timezone.make_aware(naive, timezone.get_current_timezone())

    def latest_payment(self):
        return self.payments.order_by("-created_at").first()

    def refresh_runtime_status(self, commit=True):
        if self.status == self.STATUS_UPCOMING and timezone.now() >= self.scheduled_datetime():
            self.status = self.STATUS_PENDING
            if commit:
                self.save(update_fields=['status'])
        return self
    
    @property
    def payment_badge(self):
        """Returns (css_class, text) tuple for template"""
        latest = self.latest_payment()
        if not latest:
            return ("unpaid", "Unpaid")

        mapping = {
            "paid": ("paid", "Paid"),
            "refund_pending": ("refund-pending", "Refund will initiate"),
            "refunded": ("refunded", "Refunded"),
            "failed": ("unpaid", "Payment failed"),
        }
        return mapping.get(latest.status, ("unpaid", "Unpaid"))
    
    
    def save(self, *args, **kwargs):
        # store user name snapshot
        if self.user:
            self.user_name = self.user.name or self.user.phone  

        # auto-update status if booking time has passed
        if self.status == self.STATUS_UPCOMING:
            if timezone.now() >= self.scheduled_datetime():
                self.status = self.STATUS_PENDING

        super().save(*args, **kwargs)





class Staff(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        null=True, blank=True,
    )
    
    name = models.CharField(max_length=100, blank=True)  
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username() or self.name or f"Staff {self.pk}"

    @staticmethod
    def available_staff_count():
        return Staff.objects.filter(is_active=True, user__is_active=True).count()






def get_available_slots(date):
    start_hour = 10
    end_hour = 18
    slots = []
    staff_count = Staff.available_staff_count()

    for hour in range(start_hour, end_hour):
        slot_time = time(hour, 0)  
        booking_count = Booking.objects.filter(date=date, slot=slot_time).count()

        slots.append({
            "time": slot_time.strftime("%H:%M"),
            "available": booking_count < staff_count
        })

    return slots
