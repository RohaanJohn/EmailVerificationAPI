from django.urls import path
from . import views

urlpatterns = [path("register", views.register, name="register"), path("login", views.login, name="login"), path("logout", views.logout, name="logout"),  path("emotionanalysis", views.emotionAnalysis, name="emotionanalysis"), path("contact", views.contact, name="contact"), path("emotion", views.emotion, name="emotion")]    
