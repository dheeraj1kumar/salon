from django.db.models import Sum
from .models import CartItem

def cart_count(request):
    if request.user.is_authenticated:
        agg = CartItem.objects.filter(user=request.user).aggregate(n=Sum("quantity"))
        count = agg["n"] or 0
        return {"cart_count": count}
    return {"cart_count": 0}