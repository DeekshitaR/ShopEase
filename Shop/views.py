from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order


# ---- HOME PAGE ----
def base(request):
    return render(request, 'base.html')


# ---- SIGN UP ----
def signup(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered. Please sign in.')
            return redirect('signin')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = fullname
        user.save()
        messages.success(request, 'Account created successfully! You can now sign in.')
        return redirect('signin')

    return render(request, 'signup.html')


# ---- SIGN IN ----
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(username=email).exists():
            messages.info(request, 'Email not found. Please sign up first.')
            return redirect('signup')

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Invalid password.')

    return render(request, 'signin.html')


# ---- SIGN OUT ----
def signout(request):
    logout(request)
    return redirect('signin')


# ---- ADD SOME DEFAULT PRODUCTS AUTOMATICALLY ----
def add_default_products():
    """Creates sample products automatically if table is empty."""
    if Product.objects.count() == 0:
        Product.objects.create(name="Men's T-Shirt", price=499, image='products/mens_tshirt.jpg')
        Product.objects.create(name="Women's Dress", price=899, image='products/womens_dress.jpg')
        Product.objects.create(name="Kids Hoodie", price=599, image='products/kids_hoodie.jpg')
        Product.objects.create(name="Smart Watch", price=1999, image='products/smart_watch.jpg')
        Product.objects.create(name="Sneakers", price=1499, image='products/sneakers.jpg')
        Product.objects.create(name="Handbag", price=999, image='products/handbag.jpg')
        Product.objects.create(name="Wireless Earbuds", price=1299, image='products/earbuds.jpg')
        Product.objects.create(name="Cap", price=299, image='products/cap.jpg')


# ---- STORE PAGE ----
@login_required
def store(request):
    add_default_products()  # ensures products exist
    products = Product.objects.all()
    return render(request, 'store.html', {'products': products})


# ---- ADD TO CART ----
@login_required
def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('store')

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('store')


# ---- CART PAGE ----
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':  # place order
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('cart')

        Order.objects.create(user=request.user, total_amount=total)
        cart_items.delete()
        messages.success(request, "🎉 Order placed successfully!")
        return redirect('cart')

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


# ---- INCREASE QUANTITY ----
@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')


# ---- DECREASE QUANTITY ----
@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


# ---- REMOVE ITEM ----
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.info(request, "Item removed from your cart.")
    return redirect('cart')
