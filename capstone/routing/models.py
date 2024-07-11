from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  pass

class Professional(models.Model):
  name=models.CharField(max_length=64)
  photo=models.ImageField(blank=True, upload_to="images/")
  banner=models.ImageField(blank=True, upload_to="images/")
  age=models.IntegerField(blank=True)
  profession=models.CharField(max_length=30)
  bio=models.CharField(max_length=200,blank=True)
  country=models.CharField(max_length=64)
  city=models.CharField(max_length=64)
  email=models.EmailField(max_length=254)
  phone=models.IntegerField()
  category=models.CharField(max_length=64)
  price=models.CharField(max_length=30, default="650/day")
  rating=models.FloatField(default=0)
  about=models.TextField(blank=True)
  work=models.TextField(blank=True)
  service=models.CharField(max_length=60, default="Building Services")
  opento=models.BooleanField(default=False)
  
  

class Photo(models.Model):
  photo=models.ImageField(upload_to="images/")
  account=models.ForeignKey(Professional, on_delete=CASCADE, related_name="posts")

class Review(models.Model):
  review=models.TextField()
  rating=models.FloatField(default=0.0)
  account=models.ForeignKey(Professional, on_delete=CASCADE, related_name="reviews")