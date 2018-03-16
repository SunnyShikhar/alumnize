from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('upload/', views.upload),
    path('home/', views.home),
    path('form/', views.form)
]