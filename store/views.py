import stripe
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# Set the Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    # --- NEW: Dynamic Filtering Logic ---
    def get_queryset(self):
        # Start with all active products
        queryset = Product.objects.filter(is_active=True)
        
        # Check if a category was requested in the URL (e.g., ?category=kurtis)
        category_slug = self.request.query_params.get('category', None)
        
        if category_slug:
            # Filter the database to only match that category slug exactly
            queryset = queryset.filter(category__slug__iexact=category_slug)
            
        return queryset

@api_view(['POST'])
def create_checkout_session(request):
    try:
        cart_items = request.data.get('items', [])
        line_items = []

        for item in cart_items:
            # Fetch actual product from DB to prevent users from hacking the price in frontend
            product = Product.objects.get(id=item['id'])
            
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f"{product.name} (Size: {item.get('size')})",
                        # Optional: Add the image URL to show in Stripe checkout
                        'images': [f"http://localhost:8000{product.image.url}"] if product.image else [],
                    },
                    'unit_amount': int(product.price * 100), # Stripe uses paise/cents (₹1 = 100 paise)
                },
                'quantity': item['quantity'],
            })

        # Add shipping flat rate if cart is under 2000
        subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
        if subtotal < 2000:
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {'name': 'Shipping Fee'},
                    'unit_amount': 9900, # ₹99.00
                },
                'quantity': 1,
            })

        # Generate Stripe session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            # Replace 5173 with 3000 if you are using Next.js/Create React App instead of Vite
            success_url='http://localhost:5173/?success=true',
            cancel_url='http://localhost:5173/cart/?canceled=true',
        )

        return Response({'checkout_url': checkout_session.url})

    except Exception as e:
        return Response({'error': str(e)}, status=400)