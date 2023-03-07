from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=50)

class Provider(models.Model):
    name = models.CharField(max_length=50)

class Article(models.Model):
    code = models.CharField(max_length=20)
    oem_code = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

class Location(models.Model):
    description = models.CharField(max_length=50)

class Stock(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()