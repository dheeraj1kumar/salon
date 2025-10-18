from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import CustomUser, OTP
from twilio.rest import Client
from django.shortcuts import redirect



@require_POST
def usersignup(request):
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    name = request.POST.get("username")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    
    if password != confirm_password:
        return JsonResponse({"success": False, "error": "Passwords do not match"})
    if password and len(password) < 6: 
        return JsonResponse({"success": False, "error": "Password must be at least 6 characters"})
    if password and len(password) > 20:
        return JsonResponse({"success": False, "error": "Password must be at most 20 characters"})
    if password and password.isspace():
        return JsonResponse({"success": False, "error": "Password cannot be only spaces"})
    
    if password and (not any(c.islower() for c in password) or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password)):
        return JsonResponse({"success": False, "error": "Password must contain at least one lowercase letter, one uppercase letter, and one digit"})
    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({"success": False,"error": "Email already registered"})
    
    if phone and not phone.startswith("+91"):
        phone = "+91" + phone

    if CustomUser.objects.filter(phone=phone).exists():
        return JsonResponse({"success": False, "error": "Phone already registered"})
    
    

    #otp
    otp_code = OTP.generate_otp()
    print("--------------------------->>",otp_code)
    OTP.objects.create(phone=phone, code=otp_code)
    print("=========",settings.TWILIO_ACCOUNT_SID)
    
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # print("twillio",TWILIO_ACCOUNT_SID)
        client.messages.create(
            body=f"Your Royal Barber OTP is {otp_code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone 
        )
    except Exception as e:
        print("hello")
        print("-----Twilio error:", e)
        return JsonResponse({"success": False, "error": "Failed to send OTP"})

    
    request.session["pending_user"] = {
        "phone": phone,
        "email": email,
        "name": name,
        "password": password
    }

    return JsonResponse({"success": True, "otp_required": True})








@require_POST
def verify_otp(request):
    phone = request.POST.get("phone")
    code = request.POST.get("otp")
    if phone and not phone.startswith("+91"):
        phone = "+91" + phone
    
    otp_obj = OTP.objects.filter(phone=phone, code=code).last()
    if not otp_obj or not otp_obj.is_valid():
        return JsonResponse({"success": False, "error": "Invalid or expired OTP"})

    pending_user = request.session.get("pending_user")
    if not pending_user or pending_user["phone"] != phone:
        return JsonResponse({"success": False, "error": "Session expired"})

    
    user = CustomUser.objects.create_user(
        phone=pending_user["phone"],
        email=pending_user["email"],
        name=pending_user["name"],
        password=pending_user["password"]
    )

    login(request, user)  
    del request.session["pending_user"]

    return JsonResponse({"success": True})








@require_POST
def userlogin(request):
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    if phone and not phone.startswith("+91"):
        phone = "+91" + phone
        
    if not phone or not password:
        return JsonResponse({"success": False, "error": "Phone and password required"})

    user = authenticate(request, username=phone, password=password)
    if user:
        login(request, user)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Invalid credentials"})









@require_POST
def userlogout(request):
    logout(request)
    redirect("/")
    return JsonResponse({"success": True})
    






def current_user(request):
    return JsonResponse({"is_authenticated": request.user.is_authenticated})
