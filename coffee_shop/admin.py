from django.contrib import admin
from .models import User, Table, Category, MenuItem, Order, OrderItem, Receipt, Payment

admin.site.register(User)
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Receipt)
admin.site.register(Payment)