from django.contrib import admin
from .models import Category, Product, ProductVariant

# This registers your models so they appear in the admin panel
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)