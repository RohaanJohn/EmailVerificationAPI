from django.urls import path
from . import views

urlpatterns = [path("register", views.register, name="register"), path("logout", views.logout, name="logout"),  path("verify", views.verify, name="verify"), path("contact", views.contact, name="contact")]    
