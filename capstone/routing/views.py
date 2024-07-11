from django.shortcuts import render
from django.http import HttpResponseRedirect
from routing.models import Professional, Photo, Review, User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import os
import json

# Create your views here.

def index(request):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  catag=set(Professional.objects.values_list("category", flat=True))
  all=Professional.objects.filter(rating__gt=4)
  return render(request, "routing/index.html",{
    "category": catag,
    "all": all
  })

def building(request):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  catag=set(Professional.objects.filter(service="Building Service").values_list("profession", flat=True))
  popular=Professional.objects.filter(service="Building Service").filter(rating__gt=4)
  return render(request, "routing/building.html",{
    "catag":catag,
    "popular": popular
  })

def decoration(request):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  catag=set(Professional.objects.filter(service="Decoration Service").values_list("profession", flat=True))
  popular=Professional.objects.filter(service="Decoration Service").filter(rating__gt=4)
  return render(request, "routing/decoration.html",{
    "catag": catag,
    "popular": popular
  })

def category(request):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  category=set(Professional.objects.values_list("category", flat=True))
  return render(request, "routing/category.html",{
    "categories": category
  })

def show(request, cate):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  prof=set(Professional.objects.filter(category=cate).values_list("profession", flat=True))
  return render(request, "routing/cate.html",{
    "professions": prof,
    "category": cate
  })

def profile(request, username):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  account=Professional.objects.get(name=username)
  rating=int(account.rating)
  photos=account.posts.all()
  review=account.reviews.all()
  others=Professional.objects.filter(category=account.category).exclude(name=username)
  if request.method=="POST":
    name=request.POST["name"]
    profession=request.POST["profession"]
    bio=request.POST["bio"]
    country=request.POST["country"]
    city=request.POST["city"]
    price=request.POST["price"]
    open = request.POST["open"] or account.opento
    if open =="True":
      open= True
    else: 
      open=False

    
    Professional.objects.filter(name=username).update(
      name=name,
      profession=profession,
      bio=bio,
      city=city,
      country=country,
      price=price,
      opento=open,
    )
    account=Professional.objects.get(name=name)
    rating=int(account.rating)
    return render(request, "routing/profile.html",{
      "account": account,
      "rating": [i for i in range(rating)],
      "photos":photos,
      "reviews": review,
    })
  return render(request, "routing/profile.html",{
    "account": account,
    "rating": [i for i in range(rating)],
    "photos":photos,
    "reviews": review,
    "others": others
  })



def new(request):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    names=Professional.objects.values_list("name", flat=True)
    pp=request.FILES["pp"]
    name=request.POST["name"]
    for aname in names:
      if aname.lower()==name.lower():
        return render(request, "routing/newprof.html", {"error": "This name has already taken !"})
    email=request.POST["email"]
    phone=request.POST["phone"]
    gender=request.POST["gender"]
    age=request.POST["age"]
    city=request.POST["city"]
    country=request.POST["country"]
    profession=request.POST["profession"]
    category=request.POST["category"]
    work=request.POST["work"]
    service=request.POST["service"]
    price=request.POST["price"]
    banner=request.FILES["bann"]
    new=Professional(
      name=name,
      photo=pp,
      email=email,
      phone=phone,
      age=age,
      city=city,
      country=country,
      work=work,
      profession=profession,
      category=category,
      service=service,
      price=price,
      banner=banner
    )
    new.save()
    return HttpResponseRedirect(reverse("routing:profile", kwargs={"username": name}))
  return render(request,"routing/newprof.html")

def upload(request):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    all=request.POST["data"]
    li=[]
    for data in json.loads(all):
      li.append(data[0])
      if data[14]=="No":
        open=False
      else:
        open=True
      new=Professional(
        name=data[0],
        profession=data[1],
        category=data[2],
        age=data[3],
        city=data[4],
        country=data[5],
        email=data[6],
        phone=data[7],
        rating=data[8],
        price=data[9],
        bio=data[10],
        about=data[11],
        work=data[12],
        service=data[13],
        opento=open
      )
      new.save()
    return render(request, "routing/test.html",{
      "data": li
    })
  return render(request, "routing/test.html")
  


def list(request,prof):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  li=Professional.objects.filter(profession=prof)
  return render(request, "routing/list.html",{
    "name": li,
    "profession": prof
  })

def about(request,username):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    about=request.POST["about"]
    Professional.objects.filter(name=username).update(about=about)
    return HttpResponseRedirect(reverse("routing:profile",kwargs={"username": username}))
  return 

def work(request,username): 
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    work=request.POST["work"]
    Professional.objects.filter(name=username).update(work=work)
    return HttpResponseRedirect(reverse("routing:profile",kwargs={"username": username}))
  return 

def sample(request,username):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    sample=request.FILES["upload"]
    profile=Professional.objects.get(name=username)
    new=Photo(photo=sample, account=profile)
    new.save()
    return HttpResponseRedirect(reverse("routing:profile",kwargs={"username": username}))
  return 

def review(request, username):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    account=Professional.objects.get(name=username)
    views=request.POST["review"]
    rate=round(float(request.POST["rate"]), 2)
    if 0<=rate<=5:
      new=Review(review=views,rating=rate, account=account)
      new.save()
      return HttpResponseRedirect(reverse("routing:profile",kwargs={"username": username}))
    else:
      return HttpResponseRedirect(reverse("routing:profile",kwargs={"username": username}))
    
  return

def search(request):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    profession=request.POST["profession"]
    category=request.POST["category"]
    city=request.POST["city"]
    country=request.POST["country"]
    all= Professional.objects.filter(
      profession=profession, 
      category=category,
      city=city,
      country=country
      )
  return render(request, "routing/search.html", {
    "all": all
  })

def banner(request, username):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    account=Professional.objects.get(name=username)
    if len(request.FILES) !=0:
      try:
        if len(account.banner)>0:
          os.remove(account.banner.path)
        account.banner=request.FILES["banner"]
      except:
        account.photo=request.FILES["pic"]
    account.save()
    return HttpResponseRedirect(reverse("routing:profile", kwargs={"username": username}))
  return


def picture(request, username):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  if request.method=="POST":
    account=Professional.objects.get(name=username)
    if len(request.FILES) !=0:
      try:
        if len(account.photo)>0:
          os.remove(account.photo.path)
        account.photo=request.FILES["pic"]
      except:
        account.photo=request.FILES["pic"]
    account.save()
    return HttpResponseRedirect(reverse("routing:profile", kwargs={"username": username}))
  return


def book(request, username):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  return HttpResponseRedirect(reverse("routing:profile", kwargs={"username": username}))

def login_view(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse("routing:index"))
  if request.method=="POST":
    username=request.POST["username"]
    password=request.POST["password"]
    user=authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("routing:index"))
    else:
      return render(request,"routing/login.html",{
        "message": "Invalid username and/or password"
      })

  return render(request,"routing/login.html")

def register(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse("routing:index"))
  if request.method=="POST":
    username=request.POST["username"]
    email=request.POST["email"]
    password=request.POST["password"]
    confirm=request.POST["confirm"]
    if password==confirm:
      try:
        user=User.objects.create_user(username, email, password)
        user.save()
      except IntegrityError as e:
        print(e)
        return render(request, "routing/register.html",{
          "error": "username and/or email has already be taken."
        })
      login(request, user)
      return HttpResponseRedirect(reverse("routing:index"))
    else:
      return render(request, "routing/register.html",{
        "message": "Password and Confirm password needs to be the Same"
      })
  return render(request, "routing/register.html")

def logout_view(request):
  if not request.user.is_authenticated:
    return render(request, "routing/login.html")
  logout(request)
  return render(request, "routing/login.html",{
    "success": "You have Successfully Logged out !"
  })