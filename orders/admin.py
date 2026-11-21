from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'full_name', 'city', 'total_price', 'created_at')
    list_filter = ('created_at', 'city')
    search_fields = ('customer__email', 'full_name', 'phone')
    inlines = [OrderItemInline]
