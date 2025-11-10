from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_detail(request):
    #Get cart
    
    cart = Cart(request)
    cart_products = cart.get_prods
    return render(request, 'cart_detail.html', {'cart_products' :cart_products})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    
    # Test for POST
    if request.POST.get('action') == 'post':
        try:
            # Get data with validation
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty', 1))  # Default to 1 if empty
            
            # Lookup product in DB
            product = get_object_or_404(Product, id=product_id)

            # Save to session
            cart.add(product=product, quantity=product_qty)

            # Get Cart Quantity
            cart_quantity = cart.__len__()
            
            # Return Response
            response = JsonResponse({'qty': cart_quantity})
            return response
            
        except (ValueError, TypeError) as e:
            # Handle conversion errors
            response = JsonResponse({'error': 'Invalid quantity'}, status=400)
            return response




def cart_delete(request):
    pass
def cart_update(request):
    pass