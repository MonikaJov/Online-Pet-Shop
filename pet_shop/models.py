import uuid
from datetime import timedelta

from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(models.Model):
    user = models.CharField(max_length=255)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, default='')
    surname = models.CharField(max_length=255, null=True, default='')
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


class SuperUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category (models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="category_photos", null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    amount = models.IntegerField()
    start_date = models.DateTimeField(auto_now=True)
    duration = models.IntegerField()

    def calculate_end_date(self):
        end_date = self.start_date + timedelta(days=self.duration)
        return end_date

    def __str__(self):
        return f"{self.amount}% off"


class Product (models.Model):

    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.FloatField()
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    has_sizes = models.BooleanField()
    has_colors = models.BooleanField()

    def __str__(self):
        return self.name


class OrderedProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    size = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ordered product for user: {self.user.username}"


class CartProduct(models.Model):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    # session_key = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} for user: {self.user.username}"


class Cart(models.Model):
    # session_key = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, related_name='carts')

    def __str__(self):
        return f"Cart for {self.user.username}"


class Order(models.Model):
    PAYMENT_CHOICES = (
        ('Credit Card', 'Credit Card'),
        ('Delivery', 'Delivery'),
    )
    processed = models.BooleanField(default=False, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    date = models.DateTimeField(auto_now=True)
    cart_products = models.ManyToManyField(OrderedProducts, related_name='products_from_cart')
    remark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order for user: {self.user.username}"
