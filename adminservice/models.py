from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Subcategory(models.Model):
    subName = models.CharField(max_length=100)
    catid = models.ForeignKey(Category,on_delete=models.CASCADE)


class Product(models.Model):
    catid = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcatid = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    prodName = models.CharField(max_length=100)
    prodDescription = models.TextField(max_length=500)
    prod_quantity = models.BigIntegerField()
    stock = models.CharField(max_length=20,default=None)
    prodImg = models.ImageField(upload_to='images/')
    prodPrice = models.DecimalField(decimal_places=2,max_digits=20,default=0.00)


class Offer(models.Model):
    prodid = models.ForeignKey(Product,on_delete=models.CASCADE)
    offername = models.CharField(max_length=100)
    startdate = models.DateField(max_length=12)
    enddate = models.DateField(max_length=12)
    discount_amt = models.DecimalField(decimal_places=2,max_digits=20,default=0.00)
    description = models.TextField(max_length=20000)
