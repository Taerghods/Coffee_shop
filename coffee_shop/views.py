from django.shortcuts import render
from .models import MenuItem, Category, Order, Receipt
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login
from .models import Order
from .forms import MenuItemForm

# def home_page(request):
#     return render(request, 'index.html')
#
# def menu_page(request):
#     return render(request, 'menu.html')
#
# def contact_page(request):
#     return render(request, 'contact.html')



def home(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    return render(request, 'index.html', {'menu_items': menu_items, 'categories': categories})


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


def menu(request):
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if item_id:
            cart = request.session.get('cart', [])
            cart.append(item_id)
            request.session['cart'] = cart
            return redirect('menu')
    return render(request, 'menu.html', {'menu_items': menu_items})


def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)  # Include request.FILES here
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuItemForm()
    return render(request, 'cafe/add_menu_item.html', {'form': form})


def edit_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)  # Include request.FILES here
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'cafe/edit_menu_item.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'cafe/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'cafe/login.html', {'form': form})


def cashier_dashboard(request):
    orders = Order.objects.filter(status='Pending')
    return render(request, 'cafe/dashboard.html', {'orders': orders})


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'cafe/order_detail.html', {'order': order})

