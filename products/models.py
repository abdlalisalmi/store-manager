from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    box_quantity = models.IntegerField()

    def __str__(self):
        return self.name
    
