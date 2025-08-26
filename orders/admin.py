from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('meal', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'restaurant', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'restaurant', 'created_at')
    search_fields = ('customer__username', 'restaurant__name', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    def order_number(self, obj):
        return obj.order_number
    order_number.short_description = 'Order #'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'meal', 'quantity', 'price')
    list_filter = ('order__status', 'meal__restaurant')
    search_fields = ('order__id', 'meal__name')
