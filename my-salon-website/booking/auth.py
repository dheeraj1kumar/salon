# utils/auth.py
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def ajax_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated and request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "code": "not_authenticated"}, status=401)
        return login_required(view_func)(request, *args, **kwargs)
    return _wrapped
