from django.contrib import admin
from .models import Category, Product, ProductVariant

# This registers your models so they appear in the admin panel
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
# store/admin.py
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Prevents empty rows from showing up by default
    readonly_fields = ['price'] # Prevents the client from accidentally changing historical prices

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'email', 'stripe_payment_intent']
    readonly_fields = ['created_at', 'stripe_payment_intent']
    inlines = [OrderItemInline]