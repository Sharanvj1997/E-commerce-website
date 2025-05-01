from django.shortcuts import render

from . models import *

from django.contrib import messages
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect

from shop.form import CustomUserForm

from django.contrib import messages

from django.http import JsonResponse


# Create your views here.

def home(request):
  products = Product.objects.filter(trending = 1)
  return render(request, "shop/index.html", {"products": products})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
import json

def login(request):
    if request.user.is_authenticated:
       redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Replace 'home' with the page you want to redirect to
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'shop/login.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully.')
    return redirect('home')




def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Success! You can login now.')
            return redirect('/login')
    return render(request, 'shop/register.html', {'form': form})



def collections(request):
    catagory=Category.objects.filter(status=0)
    for cat in catagory:
        print(cat.image.url)
    return render(request,'shop/collection.html',{"catagory":catagory})


def collections_view(request, name):
  if(Category.objects.filter(name = name, status = 0)):
      products = Product.objects.filter(category__name = name)
      return render(request, "shop/products/index.html",  {"products": products, "category_name": name})
  else:
    messages.warning(request, "No Such Category Found")
    return redirect('collections')
  

def product_details(request, cname, pname):
    if(Category.objects.filter(name = cname, status = 0)):
      if(Product.objects.filter(name = pname, status = 0)):
        products = Product.objects.filter(name = pname, status = 0).first()
        return render(request, "shop/products/product_details.html", {"products": products})
      else:
        messages.error(request, "No Such Produtct Found")
        return redirect('collections')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('collections')


from django.http import JsonResponse
import json
from .models import Product, Cart  # Adjust import to your models

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'not_logged_in', 'message': 'Login to add items to cart'}, status=401)

        try:
            data = json.loads(request.body)
            product_qty = int(data['product_qty'])
            product_id = data['pid']

            product = Product.objects.get(id=product_id)

            if Cart.objects.filter(user=request.user, product=product).exists():
                return JsonResponse({'status': 'error', 'message': 'Product already in cart'})

            if product.quantity >= product_qty:
                Cart.objects.create(user=request.user, product=product, product_qty=product_qty)
                return JsonResponse({'status': 'success', 'message': 'Added to cart'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Stock not available'})

        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Access'}, status=400)

def view_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'shop/cart.html', {'cart': cart})
    else:
        return redirect('home')  # ADD return here

from django.shortcuts import get_object_or_404, redirect
from .models import Cart

def remove_cart(request, cid):
    cart_item = get_object_or_404(Cart, id=cid, user=request.user)
    cart_item.delete()
    return redirect('/view_cart')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Favourite, Product

@csrf_exempt
def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'not_logged_in', 'message': 'Login to add to favourites'}, status=401)

        try:
            data = json.loads(request.body)
            product_id = data.get('pid')

            product = Product.objects.get(id=product_id)

            # Check if already in favourites
            if Favourite.objects.filter(user=request.user, product=product).exists():
                return JsonResponse({'status': 'error', 'message': 'Already in favourites'})

            Favourite.objects.create(user=request.user, product=product)
            return JsonResponse({'status': 'success', 'message': 'Added to favourites'})

        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Access'}, status=400)


    

  
from django.shortcuts import render, redirect
from .models import Favourite  # Assuming the Favourite model is in the same app

def view_fav(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, 'shop/favourites.html', {'fav': fav})
    else:
        return redirect('home')  # Redirect to home if user is not authenticated
    

from django.http import JsonResponse
from .models import Favourite

def remove_from_fav(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        product_id = data.get('product_id')

        try:
            favourite = Favourite.objects.get(user=request.user, product_id=product_id)
            favourite.delete()
            return JsonResponse({'status': 'success', 'message': 'Product removed from favourites'})
        except Favourite.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found in favourites'})

    return JsonResponse({'status': 'error', 'message': 'Unauthorized or invalid request'})

