from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Category, Order, Receipt, OrderItem
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login
from .forms import MenuItemForm



# Create your views here.
def home(request):
    menu_items = MenuItem.objects.select_related('category').all()
    return render(request, 'index.html', {'menu_items': menu_items})

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


def menu(request):
    menu_items = MenuItem.objects.all()
    categories = Category.objects.prefetch_related('menuitem_set').all()
    category_id = request.GET.get('category_id')
    if category_id:
        menu_items = menu_items.filter(category_id=category_id)
    return render(request, 'menu.html', {'menu_items': menu_items, 'categories': categories})

cart = []
def add_to_cart(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    cart.append(item)
    return redirect('menu')

def view_cart(request):
    order_items = OrderItem.objects.all()
    menu_items = OrderItem.objects.select_related('menu_item').all()
    orders = OrderItem.objects.select_related('order').all()
    return render(request, 'cart.html', {'menu_items': menu_items,'orders': orders, 'order_items': order_items, 'cart': cart})

def order_view(request):
    orders = Order.objects.all()
    return render(request, 'order.html', {'orders': orders})

def create_order(request):
    order = Order.objects.create()
    for item in cart:
        order.menu_items.add(item)
    cart.clear()
    # return redirect('order')
    return render(request, 'order.html', {'order': order})


def mark_order_ready(request, order_id):
    order = Order.objects.get(id=order_id)
    order.ready = True
    order.save()
    return redirect('order')

def receipt(request):
    context = {}
    vat = 0.10
    receipt = Receipt.objects.select_related('order').all()
    table = Order.objects.select_related('table').all()
    user = Order.objects.select_related('user').all()
    order_items = OrderItem.objects.select_related('menu_item').all()
    order = Order.objects.prefetch_related('orderitem_set').all()
    final_price = 0
    for i in receipt:
        if i.order.menu_item.discount == 0:
            i.total_price = i.order.menu_item.price * i.order.orderitem_set.quantity
        else:
            i.total_price =  i.orderitem_set.quantity * (i.order.menu_item.price - (i.order.menu_item.price * (i.order.menu_item.discount/100)))
        final_price += i.total_price
        if not user.discount == 0:
            final_price -= final_price * user.discount
            messages = "Happy Birthday!"
        else:
            messages = "0"

        i.final_price = final_price
        i.save()

        vat_amount = final_price * vat

        context = {
            'receipt': receipt,
            'table': table,
            'user': user,
            'order_items': order_items,
            'order': order,
            'vat_amount': vat_amount,
            'final_price': final_price,
            'messages': messages
        }
    return render(request, 'receipt.html', context)


# def add_to_cart(request, item_id):
#     item = MenuItem.objects.get(id=item_id)
#     if request.method == 'POST':
#         item_id = request.POST.get(item)
#         if item_id:
#             cart = request.session.get('cart', {})
#             cart[item_id] = cart.get(item_id, 0) + 1
#             request.session['cart'] = cart
#             return render(request,'receipt.html', {'cart': cart})
#     return redirect('menu')

# def cart(request):
#     menu_items = MenuItem.objects.all()
#     cart = request.session.get('cart', [])
#
#     # Check if the product is already in the cart
#     product_exists = False
#     for item in cart:
#         if item['name'] == menu_items.name: # Compare by product name instead of ID
#             item['quantity'] += 1
#             product_exists = True
#             break
#
#     # If product is not in the cart, add it
#         if not product_exists:
#             cart.append({
#             'name': menu_items.name,
#             'price': menu_items.price,
#             'quantity': 1
#             })
#
#     # Save the cart back to the session
#     request.session['cart'] = cart
#     request.session.modified = True # Mark session as modified to ensure saving
#
#     return redirect('cart')

# def cart(request, menuitem_id):
#     response.set_cookie('menuitem_id', menuitem_id)
#     return request
#
# def set_session(request):
# 	request.session['username'] = 'mostafa'
# 	request.session['user_id'] = 12345
# 	request.session['is_logged_in'] = True
# 	return render(request, 'set_session.html')
#
# def get_session(request):
#     username = request.session.get('username', 'Guest')  # Default to 'Guest' if not set
#     is_logged_in = request.session.get('is_logged_in', False)
#     request.session.set_expiry(300)
#     return render(request, 'get_session.html', {'username': username, 'is_logged_in': is_logged_in})
#
# def view_cart(request):
#     response = request.COOKIES.get('menuitem_id', '')
#     return render(request, 'receipt.html', {'menuitem_id': response})

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
    return render(request, 'register.html', {'form': form})


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
    return render(request, 'login.html', {'form': form})


def cashier_dashboard(request):
    orders = Order.objects.filter(status='Pending')
    return render(request, 'cafe/dashboard.html', {'orders': orders})


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'cafe/order_detail.html', {'order': order})



def payment(request):
    if request.method == 'POST':
        return redirect('menu')
    return render(request, 'payment.html')