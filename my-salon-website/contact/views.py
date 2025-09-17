from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt  
from django.shortcuts import render
from booking.auth import ajax_login_required
from .models import Contact


@require_POST
@ajax_login_required
def contact(request):
    data = {}
    if request.content_type and "application/json" in request.content_type:
        try:
            import json
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({"success": False, "error": "Invalid JSON body"}, status=400)
    else:
        data = request.POST

    name = (data.get("name") or "").trim() if hasattr(str, "trim") else (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    message = (data.get("message") or "").strip()

    if not name:
        return JsonResponse({"success": False, "error": "Name is required."}, status=400)
    if not message:
        return JsonResponse({"success": False, "error": "Message is required."}, status=400)
    if email:
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"success": False, "error": "Invalid email address."}, status=400)

    clean_message = strip_tags(message)

    Contact.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=clean_message
    )
    return JsonResponse({"success": True})