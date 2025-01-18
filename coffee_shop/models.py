from datetime import date

from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

class User(models.Model):
    first_name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(3)
        ]
    )
    last_name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(3)
        ]
    )
    phone_number = models.CharField(max_length=11)
        # max_length=11,
        # validators=[
        #     RegexValidator(
        #         regex=r'^\d{9}$',
        #         message='شماره تلفن باید 10 رقم باشد.'
        #     )
        # ],
        # help_text="فقط 10 رقم شماره تلفن را وارد کنید (بدون +98)."
    # )

    # def save(self, *args, **kwargs):
    #     if not self.phone_number.startswith('+98'):
    #         self.phone_number = f"+98{self.phone_number}"
    #     super().save(*args, **kwargs)

    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(9, message="رمز عبور باید حداقل ۸ کاراکتر باشد."),
            RegexValidator(
                regex=r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){8,16}$',
                message='رمز عبور باید حداقل شامل یک حرف کوچک، یک حرف بزرگ، یک عدد و یک کاراکتر خاص باشد.'
            )
        ],
        help_text="رمز عبور باید حداقل ۸ کاراکتر و ترکیبی از حروف، اعداد و کاراکترهای خاص باشد."
    )

    birthday = models.DateField(null=True, blank=True)

    def __str__(self):  
        return f"{self.first_name} {self.last_name}"

    # @property
    # def age(self):
    #         age = date.today().year
    #         return age - self.birthday


class Table(models.Model):  
    table_number = models.PositiveIntegerField(unique=True)
    cafe_space_position = models.CharField(max_length=50)  

    def __str__(self):  
        return f"Table {self.table_number}"  

class Category(models.Model):  
    name = models.CharField(max_length=50)  

    def __str__(self):  
        return self.name  

class MenuItem(models.Model):  
    name = models.CharField(max_length=100)  
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  
    description = models.TextField(null=True, blank=True)  
    serving_time_period = models.CharField(max_length=50, null=True, blank=True)
    estimated_cooking_time = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    def __str__(self):  
        return self.name  

class Order(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    table = models.ForeignKey(Table, on_delete=models.CASCADE)  
    menu_items = models.ManyToManyField(MenuItem, through='OrderItem')  
    status = models.CharField(max_length=20, default='Pending')  
    timestamp = models.DateTimeField(auto_now_add=True)  

class OrderItem(models.Model):  
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)  
    quantity = models.IntegerField()  

class Receipt(models.Model):  
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)  

class Payment(models.Model):  
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    payment_method = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):  
        return f"Payment for Receipt {self.receipt.id}"