from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, create_checkout_session

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
# NEW: Added basename='product' so Django knows how to name these URLs
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('create-checkout-session/', create_checkout_session, name='checkout'),
]