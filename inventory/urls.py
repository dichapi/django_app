from django.urls import path
from .views import create_product, update_stock, create_order

urlpatterns = [
    path('products', create_product, name='create_product'),
    path('inventories/product/<int:product_id>', update_stock, name='update_stock'),
    path('orders', create_order, name='create_order')
]
