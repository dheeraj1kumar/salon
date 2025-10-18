from datetime import datetime, timedelta, time as dtime
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST
from .auth import ajax_login_required
from dashboard.models import Service  
from .models import CartItem, Booking, Staff
from django.db.models import F, Sum
from django.contrib import messages
from .models import CartItem


SLOT_START_HOUR = 10                 
SLOT_END_HOUR = 21                   
SLOT_MINUTES_STEP = 30               
BOOKING_LEAD_MINUTES = 15 
DAYS_TO_SHOW = 7                     


SHOW_ONLY_FREE_SLOTS = False



def iter_slot_times(start_hour=SLOT_START_HOUR, end_hour=SLOT_END_HOUR, step=SLOT_MINUTES_STEP):
   
    h, m = start_hour, 0
    while True:
        if h >= end_hour and m > 0:
            break
        yield dtime(h, m)
        m += step
        if m >= 60:
            m -= 60
            h += 1
        if h > end_hour:
            break

def staff_capacity_on(date_obj):
   
    return Staff.available_staff_count()

def _overlaps(a_start, a_end, b_start, b_end):
    
    return a_start < b_end and b_start < a_end

def _intervals_for_day(date_obj):
    
    qs = (Booking.objects.filter(date=date_obj).exclude(status=Booking.STATUS_CANCELED).select_related("service"))
    intervals = []
    for b in qs:
        start_dt = datetime.combine(date_obj, b.slot)
        dur = b.service.duration or timedelta(minutes=60)
        end_dt = start_dt + dur
        intervals.append((start_dt, end_dt))
    return intervals

def cart_combined_duration(cart_items):
    
    total = timedelta()
    for ci in cart_items:
        dur = ci.service.duration or timedelta(minutes=60)
        total += (dur * ci.quantity)
    return total

def slots_with_status_duration_aware(date_input):
    
    date_obj = datetime.strptime(date_input, "%Y-%m-%d").date() if isinstance(date_input, str) else date_input
    capacity = staff_capacity_on(date_obj)
    intervals = _intervals_for_day(date_obj)

    
    now_local = localtime()
    cutoff_time = (now_local + timedelta(minutes=BOOKING_LEAD_MINUTES)).time() if date_obj == now_local.date() else None

    out = []
    step_delta = timedelta(minutes=SLOT_MINUTES_STEP)
    for t in iter_slot_times():
        if cutoff_time and t < cutoff_time:
            continue
        cell_start = datetime.combine(date_obj, t)
        cell_end = cell_start + step_delta
        used = 0
        for s, e in intervals:
            if _overlaps(cell_start, cell_end, s, e):
                used += 1
        remaining = max(capacity - used, 0)
        out.append({"time": t, "available": remaining > 0, "remaining": remaining})
    return out




def start_cells_that_fit(date_str, duration, capacity=None):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if isinstance(date_str, str) else date_str
    capacity = capacity or staff_capacity_on(date_obj)
    intervals = _intervals_for_day(date_obj)

    now_local = localtime()
    cutoff_time = (now_local + timedelta(minutes=BOOKING_LEAD_MINUTES)).time() if date_obj == now_local.date() else None

    step = timedelta(minutes=SLOT_MINUTES_STEP)
    closing_dt = datetime.combine(date_obj, dtime(SLOT_END_HOUR, 0))

    out = []
    for t in iter_slot_times():
        if cutoff_time and t < cutoff_time:
            continue

        session_start = datetime.combine(date_obj, t)
        session_end = session_start + duration

        
        if session_end > closing_dt:
            continue

        cursor = session_start
        ok = True
        worst_remaining = capacity
        while cursor < session_end:
            cell_end = min(cursor + step, session_end)
            used = 0
            for s, e in intervals:
                if _overlaps(cursor, cell_end, s, e):
                    used += 1
            remaining = capacity - used
            if remaining <= 0:
                ok = False
                break
            worst_remaining = min(worst_remaining, remaining)
            cursor = cell_end

        if ok:
            out.append({"time": t, "available": True, "remaining": max(0, worst_remaining)})

    return out





@require_POST
@ajax_login_required
def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    item, created = CartItem.objects.get_or_create(user=request.user, service=service)
    if created:
        item.quantity = 1
        item.save()
        status, message = "added", f"{service.name} added to cart."
    else:
        if item.quantity != 1:
            item.quantity = 1
            item.save()
        status, message = "exists", f"{service.name} is already in cart."

    agg = CartItem.objects.filter(user=request.user).aggregate(n=Sum("quantity"))
    count = agg["n"] or 0
    return JsonResponse({"success": True, "status": status, "message": message, "cart_count": count})




@ajax_login_required
def update_cart_item(request, item_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    try:
        qty = int(request.POST.get("quantity", "1"))
    except ValueError:
        qty = 1
    item.quantity = max(1, qty)
    item.save()
    return redirect("view_cart")





@ajax_login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("service")

    
    for ci in cart_items:
        ci.line_total = ci.service.price * ci.quantity
    total = sum(ci.line_total for ci in cart_items)

    
    today = localtime().date()
    dates = [today + timedelta(days=i) for i in range(DAYS_TO_SHOW)]

    
    raw_qs_date = request.GET.get("date")
    if raw_qs_date:
        try:
            selected_date = datetime.strptime(raw_qs_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    if selected_date < today or selected_date > dates[-1]:
        selected_date = today

    selected_date_str = selected_date.strftime("%Y-%m-%d")

    
    if raw_qs_date and raw_qs_date != selected_date_str:
        query = urlencode({"date": selected_date_str})
        return redirect(f"{request.path}?{query}")

    capacity = staff_capacity_on(selected_date)

    
    combined_dur = cart_combined_duration(cart_items)

    if combined_dur.total_seconds() > 0:
        
        start_status = start_cells_that_fit(selected_date_str, combined_dur, capacity)
        if SHOW_ONLY_FREE_SLOTS:
            slots = [s["time"].strftime("%H:%M") for s in start_status]
            slot_status = []
        else:
            slot_status = start_status
            slots = []
    else:
        
        slot_status, slots = [], []

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total,
        "dates": dates,
        "selected_date": selected_date_str,
        "slots": slots,                 
        "slot_status": slot_status,     
    })


@ajax_login_required
def slots_api(request):
    
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"slots": [], "mode": "none"})

    cart_items = CartItem.objects.filter(user=request.user).select_related("service")
    combined_dur = cart_combined_duration(cart_items)
    if combined_dur.total_seconds() <= 0:
        return JsonResponse({"mode": "status", "slots": []})

    capacity = staff_capacity_on(datetime.strptime(date_str, "%Y-%m-%d").date())
    start_status = start_cells_that_fit(date_str, combined_dur, capacity)

    if SHOW_ONLY_FREE_SLOTS:
        return JsonResponse({
            "mode": "free_only",
            "slots": [s["time"].strftime("%H:%M") for s in start_status]
        })
    else:
        payload = [{
            "time": s["time"].strftime("%H:%M"),
            "label": s["time"].strftime("%I:%M %p"),
            "available": s["available"],
            "remaining": s["remaining"],
        } for s in start_status]
        return JsonResponse({"mode": "status", "slots": payload})





from random import shuffle
@ajax_login_required
def confirm_booking(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request"})

    
    date_str = request.POST.get("date")   # 'YYYY-MM-DD'
    slot_str = request.POST.get("slot")   # 'HH:MM'
    if not date_str or not slot_str:
        return JsonResponse({"success": False, "error": "Missing date or slot"})

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        hour, minute = map(int, slot_str.split(":"))
        slot_time = dtime(hour, minute)
    except Exception:
        return JsonResponse({"success": False, "error": "Bad date/slot"})

    
    now_local = localtime()
    if date_obj == now_local.date():
        cutoff = (now_local + timedelta(minutes=BOOKING_LEAD_MINUTES)).time()
        if slot_time < cutoff:
            return JsonResponse({"success": False, "error": "Selected time has passed."})

    
    cart_items = CartItem.objects.filter(user=request.user).select_related("service")
    if not cart_items.exists():
        return JsonResponse({"success": False, "error": "Cart is empty"})

    
    def cart_combined_duration(cart_qs):
        total = timedelta()
        for ci in cart_qs:
            dur = ci.service.duration or timedelta(minutes=60)
            total += (dur * ci.quantity)
        return total

    combined_dur = cart_combined_duration(cart_items)
    if combined_dur.total_seconds() <= 0:
        return JsonResponse({"success": False, "error": "Cart has no timed services."})

    session_start = datetime.combine(date_obj, slot_time)
    session_end = session_start + combined_dur

    
    closing_dt = datetime.combine(date_obj, dtime(SLOT_END_HOUR, 0))
    if session_end > closing_dt:
        return JsonResponse({"success": False, "error": "Session extends beyond closing time. Choose an earlier slot."})

    
    with transaction.atomic():
       
        existing = (Booking.objects
                    .select_for_update()
                    .filter(date=date_obj)
                    .select_related("service", "staff"))

        
        staff_qs = Staff.objects.select_for_update().all()
        candidate_staff_ids = list(staff_qs.values_list('id', flat=True))

       
        from collections import defaultdict
        existing_intervals_by_staff = defaultdict(list)
        for b in existing.exclude(status=Booking.STATUS_CANCELED):
            b_start = datetime.combine(date_obj, b.slot)
            b_dur = b.service.duration or timedelta(minutes=60)
            b_end = b_start + b_dur
            if b.staff_id:
                existing_intervals_by_staff[b.staff_id].append((b_start, b_end))

        def staff_is_free(staff_id, s_dt, e_dt):
            for (bs, be) in existing_intervals_by_staff.get(staff_id, []):
                if _overlaps(s_dt, e_dt, bs, be):
                    return False
            return True

        def pick_random_staff_for_interval(s_dt, e_dt):
            ids = candidate_staff_ids[:]  
            shuffle(ids)
            for sid in ids:
                if staff_is_free(sid, s_dt, e_dt):
                    return sid
            return None

        
        cursor = session_start
        created_ids = []
        for item in cart_items:
            dur = item.service.duration or timedelta(minutes=60)
            for _ in range(item.quantity):
                seg_start = cursor
                seg_end = cursor + dur

                staff_id = pick_random_staff_for_interval(seg_start, seg_end)
                if staff_id is None:
                    transaction.set_rollback(True)
                    return JsonResponse({
                        "success": False,
                        "error": "No staff available for the selected time."
                    })

                booking = Booking.objects.create(
                    user=request.user,
                    service=item.service,
                    date=date_obj,
                    slot=seg_start.time(),
                    status=Booking.STATUS_UPCOMING,
                    staff_id=staff_id,
                    price=item.service.price,
                    payment_status=Booking.PAYMENT_NONE,
                )
                created_ids.append(booking.id)

                
                existing_intervals_by_staff[staff_id].append((seg_start, seg_end))
                cursor += dur

        
        cart_items.delete()

    return JsonResponse({"success": True, "message": "Booking confirmed!", "booking_ids": created_ids})










def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"

def cart_total_for(user):
    total = (
        CartItem.objects
        .filter(user=user)
        .aggregate(sum=Sum(F("quantity") * F("service__price")))  
        .get("sum") or 0
    )
    return total




@ajax_login_required
@require_POST
def remove_from_cart(request, item_id):
    try:
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.delete()

        if is_ajax(request):
            total = cart_total_for(request.user)
            return JsonResponse({
                "status": "success",
                "message": "Item removed from cart.",
                "total": total
            }, status=200)

        messages.success(request, "Item removed from cart.")
        return redirect("view_cart")

    except CartItem.DoesNotExist:
        if is_ajax(request):
            return JsonResponse({"status": "error", "message": "Item not found."}, status=404)
        messages.error(request, "Item not found.")
        return redirect("view_cart")

    except Exception:
        if is_ajax(request):
            return JsonResponse({"status": "error", "message": "Could not remove item."}, status=400)
        messages.error(request, "Could not remove item.")
        return redirect("view_cart")

