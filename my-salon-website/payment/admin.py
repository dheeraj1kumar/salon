from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "order_id", "user", "amount", "currency", 
        "gateway", "status", "created_at"
    )
    list_filter = ("gateway", "status", "currency", "created_at")
    search_fields = (
        "order_id", "payment_id", "refund_id",
        "user__username", "user__email",
        "bookings__id", "bookings__service__name"  
    )
    readonly_fields = ("created_at", "updated_at")

    ordering = ("-created_at",)

   
    def get_bookings(self, obj):
        return ", ".join(str(b.id) for b in obj.bookings.all())
    get_bookings.short_description = "Bookings"
