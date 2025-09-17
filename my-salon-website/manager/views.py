from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from booking.models import Booking,Staff
from dashboard.models import Service
from django.utils import timezone
from django.contrib import messages
from .forms import ServiceForm, StaffForm
from datetime import timedelta
from decimal import Decimal
import razorpay
from payment.models import Payment
from payment.services import get_razorpay_client

def is_staff(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff)
def dashboard(request):
    today = timezone.localdate()
    two_days_ago = today - timedelta(days=2)

    past_bookings = Booking.objects.filter(date__gte=two_days_ago, date__lt=today).order_by('-date')[:15]
    todays_bookings = Booking.objects.filter(date=today).order_by('slot')
    upcoming_bookings = Booking.objects.filter(date__gt=today).order_by('date')

    
    service_form = ServiceForm()
    staff_form = StaffForm()

    context = {
        'past_bookings': past_bookings,
        'todays_bookings': todays_bookings,
        'upcoming_bookings': upcoming_bookings,
        'service_form': service_form,
        'staff_form': staff_form,
    }
    return render(request, 'admin.html', context)


def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully!')
        else:
            messages.error(request, 'Error adding service.')
    return redirect('dashboard')


def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff added successfully!')
        else:
            messages.error(request, 'Error adding staff.')
    return redirect('dashboard')










@user_passes_test(lambda u: u.is_staff)
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)

    
    if booking.status in [Booking.STATUS_COMPLETED, Booking.STATUS_CANCELED]:
        messages.warning(request, "This booking is already finalized and cannot be changed.")
        return redirect("dashboard")

   
    if status == Booking.STATUS_CANCELED:
        booking.status = Booking.STATUS_CANCELED
        booking.is_paid = False   

        payment = booking.latest_payment()

        if payment and payment.status == Payment.STATUS_PAID and payment.payment_id:
            client = get_razorpay_client()
            amount_paise = int(booking.price * 100)  

            try:
                refund = client.payment.refund(payment.payment_id, {"amount": amount_paise})

                
                booking.payment_status = Booking.PAYMENT_REFUND_PENDING
                booking.refund_id = refund.get("id")
                booking.refund_amount = booking.price
                booking.save(update_fields=["payment_status", "refund_id", "refund_amount"])

                
                
                if refund.get("status") in ("processed", "completed", "succeeded"):
                    booking.is_paid=False
                    booking.status=Booking.STATUS_CANCELED
                    booking.payment_status = Booking.PAYMENT_REFUNDED
                    booking.save(update_fields=["payment_status","is_paid", "status",])

                messages.success(request, f"Booking canceled. Refund of ₹{booking.price} initiated.")

            except razorpay.errors.BadRequestError:
                messages.error(request, "Refund request failed. Support will assist you.")
            except Exception as e:
                messages.error(request, f"Could not initiate refund right now: {str(e)}")
        else:
            
            booking.payment_status = Booking.PAYMENT_NONE
            booking.save(update_fields=["status", "is_paid", "payment_status"])
            messages.success(request, "Booking canceled (no online payment found).")

    
    elif status == Booking.STATUS_COMPLETED:
        booking.status = Booking.STATUS_COMPLETED
        booking.save(update_fields=['status'])
        messages.success(request, "Booking marked as completed.")

    return redirect("dashboard")

