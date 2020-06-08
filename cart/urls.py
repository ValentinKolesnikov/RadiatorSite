from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart_view, name="cart_view"),
    path('add/', views.add_product_view, name="add_product_view"),
    path('remove/', views.remove_product_view, name="remove_product_view"),
    path('change-quantity/', views.change_quantity_view, name="change_quantity_view"),
    path('send-mail/', views.send_mail_view, name="send_mail_view"),
    path('checkout/', views.checkout_view, name="checkout_view"),

]
