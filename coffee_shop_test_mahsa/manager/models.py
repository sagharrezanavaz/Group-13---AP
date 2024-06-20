from django.db import models

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class ProductMaterial(models.Model):
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE)
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.material.name}'
