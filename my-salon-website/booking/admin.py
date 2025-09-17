from django.contrib import admin
from .models import Booking,CartItem,Staff

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_name', 'service', 'date', 'slot', 'status', 'created_at')
    list_filter = ('status', 'date', 'service')
    search_fields = ('user_name', 'service__name')
    readonly_fields = ('user_name',)
    actions = ['mark_completed', 'mark_canceled']

    @admin.action(description="Mark selected bookings as completed")
    def mark_completed(self, request, queryset):
        updated = queryset.update(status=Booking.STATUS_COMPLETED)
        self.message_user(request, f"{updated} booking(s) marked as completed")

    @admin.action(description="Mark selected bookings as canceled")
    def mark_canceled(self, request, queryset):
        updated = queryset.update(status=Booking.STATUS_CANCELED)
        self.message_user(request, f"{updated} booking(s) marked as canceled")



admin.site.register(CartItem)
admin.site.register(Staff)