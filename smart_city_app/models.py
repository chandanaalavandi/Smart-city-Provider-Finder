from django.db import models

# Create your models here.
class User_Registration(models.Model):
    full_name=models.CharField(max_length=20)
    emailid=models.CharField(max_length=20)
    phoneno=models.CharField(max_length=20)
    birthdate=models.CharField(max_length=20)
    address=models.CharField(max_length=500)
    password=models.CharField(max_length=20)

class Service_Registration(models.Model):
    service_name=models.CharField(max_length=20)


class Service_Provider(models.Model):
    full_name=models.CharField(max_length=20)
    emailid=models.CharField(max_length=20)
    phoneno=models.CharField(max_length=20)
    birthdate=models.CharField(max_length=20)
    address=models.CharField(max_length=500)
    password=models.CharField(max_length=20)


class Add_Shops(models.Model):
    emailid=models.CharField(max_length=20)
    shop_category=models.CharField(max_length=20)
    city_name=models.CharField(max_length=20)
    shop_name=models.CharField(max_length=25)
    owner_name=models.CharField(max_length=25)
    contact_number=models.CharField(max_length=20)
    services=models.CharField(max_length=200)
    shop_photo=models.ImageField(upload_to='shop_photo/')
    others_photo=models.ImageField(upload_to='shop_photos/')
    owner_photo=models.ImageField(upload_to='owner_photos/')
    open_clode=models.CharField(max_length=20)
    area=models.CharField(max_length=15)
    latitude=models.CharField(max_length=20)
    longitude=models.CharField(max_length=20)
    address=models.CharField(max_length=100)
