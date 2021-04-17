from django.db import models
from django.utils import timezone

from adminservice.models import Product


class User_register(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=200)

class Cart(models.Model):
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    userid = models.ForeignKey(User_register, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    quantity = models.BigIntegerField()


    def add(self, product):
        pass

    def remove(self, product):
        pass

    def decrement(self, product):
        pass

    def clear(self):
        pass

class Billaddress(models.Model):
    userid = models.ForeignKey(User_register,on_delete=models.CASCADE)
    mobile = models.BigIntegerField()
    pincode = models.IntegerField()
    address = models.TextField()
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)



class Payment(models.Model):
    userid = models.ForeignKey(User_register,on_delete=models.CASCADE)
    cardName = models.CharField(max_length=100)
    cardNo = models.CharField(max_length=12)
    expirationDate = models.DateField()


class Contact(models.Model):
    userid = models.ForeignKey(User_register, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=20000)

class Order(models.Model):
    orderid = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    userid = models.ForeignKey(User_register, on_delete=models.CASCADE)
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    quantity = models.BigIntegerField()
    Payment_status= models.CharField(max_length=20, null=True, blank=True)
    Datetime_of_payment = models.DateTimeField(default=timezone.now)
    Payment_mode = models.CharField(max_length=20)
    Success_mode = models.CharField(max_length=20)

class User_feedback(models.Model):
    userid = models.ForeignKey(User_register, on_delete=models.CASCADE)
    prodid = models.ForeignKey(Product, on_delete=models.CASCADE)
    Datetime_of_feedback = models.DateTimeField(default=timezone.now)
    feedback_message = models.TextField(max_length=10000)



