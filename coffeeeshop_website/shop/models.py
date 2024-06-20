

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField()

class Product(models.Model):
    VERTICAL_CHOICES = [
        ('hot_drinks', 'Hot Drinks'),
        ('cold_drinks', 'Cold Drinks'),
        ('cakes', 'Cakes'),
    ]

    name = models.CharField(max_length=100)
    vertical = models.CharField(max_length=20, choices=VERTICAL_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    raw_materials = models.ManyToManyField(RawMaterial, through='ProductMaterial')

class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.FloatField()

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    delivery_option = models.CharField(max_length=50, choices=[('in_place', 'In Place'), ('delivery', 'Delivery')])
    created_at = models.DateTimeField(auto_now_add=True)
