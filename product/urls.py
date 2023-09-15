from django.urls import path
from .add_product_view import upload_view

urlpatterns = [
    path('add-products', upload_view, name="AddProduct"),
]

