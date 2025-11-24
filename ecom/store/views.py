from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import Shippingform
from payment.models import ShippingAddress
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.
def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains =searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	



def update_info(request):
    if request.user.is_authenticated:
        # Get current user profile
        current_user = Profile.objects.get(user__id=request.user.id)

        # Get user shipping info 
        # NOTE: Usually this is ShippingAddress.objects.get(user=request.user)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        # Get forms
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = Shippingform(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            # Save both forms
            form.save()
            shipping_form.save()
            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')

        return render(request, "update_info.html", {
            'form': form,
            'shipping_form': shipping_form
        })

    else:
        messages.error(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')




def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "You password is successfully updated.")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(request, 'update_password.html',{'form': form})
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html',{'form': form})
    else:
        messages.success(request,"You ust be logged in to visit this page.")
        return redirect('home')

def user_update(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User is updated successfully.")
            return redirect('home')
        return render(request, 'user_update.html', {'user_form': user_form})
    else:
        messages.success(request, "User must login to access it.")
        return redirect('home')
        

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

# for categories

def category(request, comm):
    #Replace Hyphrns with spces
    comm = comm.replace('-', ' ')
    try:
        category = Category.objects.get(name__iexact=comm)
        products = Product.objects.filter(category = category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, "This  category doesn't exists")
        return redirect('home')
    
def categroy_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
        if user is not None:
            login(request, user)

            # Do some sopping cart stuff
            current_user = Profile.objects.get(user__id = request.user.id)
            # get their saved cart from db
            saved_cart = current_user.old_cart

            # Convert database string to python dictionary using json
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                 # Add the loaded cart dictionary to our session
                 # Get the cart
                cart = Cart(request)
                #  loop through the cart and add the items from the database
                for key, value in converted_cart.items():
                     cart.db_add(product = key, quantity = value)

            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.success(request, "Username or Password you entered is incorrect. Pleasr try again.")
            return redirect('login')
            
    return render(request, 'login.html', {})

def logout_view(request):
      logout(request)
      messages.success(request, "You have been sucessfully Logout.")
      return redirect('home')

def register(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
          form = SignUpForm()
          return render(request, 'register.html',{'form':form})