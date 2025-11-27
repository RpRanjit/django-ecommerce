from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import Shippingform, PaymentForm
from payment.models import ShippingAddress,Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product
# Create your views here.

def process_order(request):

    if request.POST:
        #Get cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities= cart.get_quants()
        totals = cart.cart_totals()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zip_code']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals
        
        # Create order
        if request.user.is_authenticated:
            #logged in
            user = request.user

            create_order = Order(user = user, full_name = full_name, email = email, shipping_address = shipping_address , amount_paid = amount_paid)
            create_order.save()

            #Get order Items
            order_id = create_order.pk
            #Get product stuff
            for product in cart_products:
                #get product id
                product_id = product.id
                # for price of product
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # %get Quanatity
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # Create an order item
                        create_order_item  = OrderItem(order_id = order_id, product_id = product_id, user = user, quntity = value, price = price)
                        create_order_item.save()



            messages.success(request, "Order Placed")
            return redirect('home')
        else:
            create_order = Order(full_name = full_name, email = email, shipping_address = shipping_address ,amount_paid = amount_paid)
            create_order.save()

            #Get order Items
            order_id = create_order.pk
            #Get product stuff
            for product in cart_products:
                #get product id
                product_id = product.id
                # for price of product
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # %get Quanatity
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # Create an order item
                        create_order_item  = OrderItem(order_id = order_id, product_id = product_id, quntity = value, price = price)
                        create_order_item.save()
            messages.success(request, "Order Placed")
            return redirect('home')

    else:
        messages.success(request, "Access Denied!!")
        return redirect('home')

def billing_info(request):
    if request.POST:
    #Get cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities= cart.get_quants()
        totals = cart.cart_totals()

        #Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check to see if user is logged in
        if request.user.is_authenticated:
			# Get The Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

        else:
			# Not logged in
			# Get The Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})	
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def checkout(request):
    #Get cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities= cart.get_quants()
    totals = cart.cart_totals()

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