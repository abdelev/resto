from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User


# Create your models here.
class Menu(models.Model):
    CATEGORY = (
        ('Starter', 'Starter'),
        ('Dish', 'Dish'),
        ('Dessert', 'Dessert'),
        ('Drinks', 'Drinks'),
    )
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=1000, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    price = models.FloatField(null=True)
    image = ResizedImageField(size=[200, 200], quality=75, upload_to='static/images/', null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name + '/' + self.category


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    menu = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.menu.name