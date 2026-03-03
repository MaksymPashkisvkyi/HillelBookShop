# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.detail, name='detail'),
    path('about/', views.about, name='about'),
    # path('cart/', views.cart_view, name='cart_view'),

]
