from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import Shippingform, PaymentForm
from payment.models import ShippingAddress
from django.contrib import messages
# Create your views here.

def billing_info(request):
    if request.POST:
    #Get cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities= cart.get_quants()
        totals = cart.cart_totals

        #Check to see if user is logged in
        if request.user.is_authenticated:
        #get the Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products' :cart_products, 'quantities': quantities, 'totals': totals,'shipping_info': request.POST, 'billing_form': billing_form})
        else:
        #if not logged in
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products' :cart_products, 'quantities': quantities, 'totals': totals,'shipping_info': request.POST, 'billing_form': billing_form})
        


        shipping_info = request.POST
        return render(request, 'payment/billing_info.html', {'cart_products' :cart_products, 'quantities': quantities, 'totals': totals,'shipping_form': request.POST})
    else:
        messages.success(request, "Access Denied!!")
        return redirect('home')

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def checkout(request):
    #Get cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities= cart.get_quants()
    totals = cart.cart_totals

    if request.user.is_authenticated:
        # Checkout as Login user
        #shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # shipping form
        shipping_form = Shippingform(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products' :cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else:
        # Checkout as Guest
        shipping_form = Shippingform(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products' :cart_products, 'quantities': quantities, 'totals': totals,'shipping_form': shipping_form})