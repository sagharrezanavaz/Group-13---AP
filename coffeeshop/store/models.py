from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Product Title")
    Sugar=models.IntegerField(verbose_name="Sugar", default=0)
    Coffee=models.IntegerField(verbose_name="Coffee", default=0)
    Flour=models.IntegerField(verbose_name="Flour", default=0)
    Chocolate=models.IntegerField(verbose_name="Chocolate", default=0)
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    short_description = models.TextField(verbose_name="Short Description")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Product Category", on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    def __str__(self):
        return str(self.user)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price



class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(
        max_length=50,
        default="Pending"
        )

class Storage(models.Model):
    name=models.CharField(max_length=255, verbose_name="Name")
    amount=models.IntegerField(verbose_name="Amount",default=0)

