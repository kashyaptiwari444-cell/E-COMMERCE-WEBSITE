from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("register/",views.register_page, name="register"),
    
    path("homepage/", views.homepage, name="homepage"),
    
    path("user_main_dash/", views.user_main_dash, name="user_main_dash"),
    path("user_dash/", views.user_dash, name="user_dash"),
    
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("remove_cart_item/<int:id>/", views.remove_cart_item, name="remove_cart_item")
        
]