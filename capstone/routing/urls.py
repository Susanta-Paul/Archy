from django.urls import path
from routing import views

app_name="routing"
urlpatterns=[
  path("", views.index, name="index"),
  path("building", views.building, name="building"),
  path("decoration",views.decoration, name="decoration"),
  path("category", views.category, name="category"),
  path("category/<str:cate>",views.show,name="category"),
  path("list/<str:prof>", views.list, name="list"),
  path("new", views.new, name="new"),
  path("profile/<str:username>/", views.profile, name="profile"),
  path("login_view", views.login_view, name="login_view"),
  path("register", views.register, name="register"),
  path("logout_view", views.logout_view, name="logout_view"),

  path("about/<str:username>", views.about, name="about"),
  path("work/<str:username>", views.work, name="work"),
  path("sample/<str:username>", views.sample, name="sample"),
  path("review/<str:username>", views.review, name="review"),
  path("search", views.search, name="search"),
  path("banner/<str:username>", views.banner, name="banner"),
  path("picture/<str:username>", views.picture, name="picture"),
  path("book/<str:username>", views.book, name="book"),

  
  path("upload",views.upload, name="upload"),
]