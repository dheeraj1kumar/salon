
import json
import razorpay
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Payment
from booking.models import Booking


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



@require_POST
def create_multiple_payment(request):
    data = json.loads(request.body)
    booking_ids = data.get("booking_ids", [])
    amount = float(data.get("amount", 0)) * 100  

    if not booking_ids or amount <= 0:
        return JsonResponse({"success": False, "error": "Invalid booking data"})

  
    order = client.order.create({
        "amount": int(amount),
        "currency": "INR",
        "payment_capture": 1,
    })

   
    payment = Payment.objects.create(
        order_id=order["id"],
        amount=Decimal(amount) / 100,
        currency="INR",
        user=request.user,
    )
    payment.bookings.set(Booking.objects.filter(id__in=booking_ids))

    return JsonResponse({
        "success": True,
        "order_id": order["id"],
        "amount": amount,
        "currency": "INR",
        "key": settings.RAZORPAY_KEY_ID,
        "name": "Royal Barber",
        "description": f"Bookings {', '.join(map(str, booking_ids))}"
    })



@csrf_exempt
def verify_payment(request, order_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"})

    data = json.loads(request.body)
    try:
       
        client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature'],
        })

        
        payment = Payment.objects.filter(order_id=order_id).first()
        if not payment:
            return JsonResponse({"success": False, "error": "Payment record not found"})

        
        payment.payment_id = data['razorpay_payment_id']
        payment.signature = data['razorpay_signature']
        payment.status = Payment.STATUS_PAID
        payment.save(update_fields=["payment_id", "signature", "status"])

        
        bookings = payment.bookings.all()
        for booking in bookings:
            booking.is_paid = True
            booking.payment_status = Booking.PAYMENT_PAID
            booking.save(update_fields=["is_paid", "payment_status"])

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


