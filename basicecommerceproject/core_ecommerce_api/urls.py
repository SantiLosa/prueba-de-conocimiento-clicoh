# from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename="products")
router.register(r'orders', views.OrderViewSet, basename="orders")
router.register(r'order-details', views.OrderDetailViewSet, basename="order-details")

urlpatterns = [
    path('', include(router.urls)),
]
