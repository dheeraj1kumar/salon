from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from booking.models import Booking


def _aware_scheduled_dt(date_obj, time_obj):
    naive = datetime.combine(date_obj, time_obj)
    return timezone.make_aware(naive, timezone.get_current_timezone())




def _can_cancel(booking, now_local=None):
    if booking.status != Booking.STATUS_UPCOMING:
        return False
    now_local = now_local or timezone.localtime()
    sched = _aware_scheduled_dt(booking.date, booking.slot)
    return now_local < (sched - timedelta(days=1))





@login_required
def my_bookings(request):
    qs = (Booking.objects
          .filter(user=request.user)
          .select_related('service', 'staff')
          .prefetch_related('payments')
          .order_by('date', 'slot'))

    
    for b in qs:
        b.refresh_runtime_status(commit=True)

    now_local = timezone.localtime()
    bookings_ctx = [{"obj": b, "can_cancel": _can_cancel(b, now_local)} for b in qs]

    today = now_local.date()
    active, past = [], []
    for ctx in bookings_ctx:
        b = ctx["obj"]
        if b.status in (Booking.STATUS_UPCOMING, Booking.STATUS_PENDING) and b.date >= today:
            active.append(ctx)
        else:
            past.append(ctx)

    return render(request, "my_booking.html", {
        "active_bookings": active,
        "past_bookings": past,
    })








from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import razorpay
from payment.models import Payment
from payment.services import get_razorpay_client

@login_required
@require_POST
def cancel_booking(request, booking_id):
    b = get_object_or_404(Booking, id=booking_id, user=request.user)

    if b.status not in (Booking.STATUS_UPCOMING, Booking.STATUS_PENDING):
        messages.error(request, "Cannot cancel this booking now.")
        return redirect("my_bookings")

   
    b.status = Booking.STATUS_CANCELED
    b.save(update_fields=["status"])

    payment = b.latest_payment()

    if payment and payment.status == Payment.STATUS_PAID and payment.payment_id:
        client = get_razorpay_client()

        refund_amount = b.price   
        amount_paise = int(refund_amount * 100)

        if amount_paise > 0:
            try:
                refund = client.payment.refund(
                    payment.payment_id,
                    {"amount": amount_paise}
                )

                b.payment_status = Booking.PAYMENT_REFUND_PENDING
                b.refund_id = refund.get("id")
                b.refund_amount = refund_amount
                b.save(update_fields=["payment_status", "refund_id", "refund_amount"])

                if refund.get("status") in ("processed", "completed", "succeeded"):
                    b.is_paid = False
                    b.status = Booking.STATUS_CANCELED
                    b.payment_status = Booking.PAYMENT_REFUNDED
                    b.save(update_fields=["is_paid", "status", "payment_status"])

                messages.success(request, f"Booking canceled. Refund of ₹{refund_amount} initiated.")
            except razorpay.errors.BadRequestError:
                messages.error(request, "Refund request failed. Support will assist you.")
            except Exception as e:
                messages.error(request, f"Could not initiate refund: {str(e)}")
        else:
            b.payment_status = Booking.PAYMENT_NONE
            b.save(update_fields=["payment_status"])
            messages.success(request, "Booking canceled (no refundable amount).")
    else:
        b.payment_status = Booking.PAYMENT_NONE
        b.save(update_fields=["payment_status"])
        messages.success(request, "Booking canceled (no payment to refund).")

    return redirect("my_bookings")
