# tasks.py
from django.utils import timezone
from .models import Booking

def promote_upcoming_to_pending():
    now = timezone.now()
    to_update = []
    for b in Booking.objects.filter(status=Booking.STATUS_UPCOMING).only('id', 'date', 'slot', 'status'):
        if now >= b.scheduled_datetime():
            to_update.append(b.id)
    if to_update:
        Booking.objects.filter(id__in=to_update).update(status=Booking.STATUS_PENDING)
