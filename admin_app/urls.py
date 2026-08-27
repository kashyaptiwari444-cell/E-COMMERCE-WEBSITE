
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dash, name="admin_dash"),
    path('admin_dash/', views.admin_dash, name="admin_dash"),
    
    path('products/add_product/', views.add_product, name="add_product"),
    path('products/view_product/', views.view_product, name="view_product"),
    path("products/edit_product/<int:id>/", views.edit_product, name="edit_product"),
    path('products/delete_product/<int:id>/', views.delete_product, name="delete_product"),
    
    path('category/add_category/', views.add_category, name="add_category"),
    path('category/view_category/', views.view_category, name="view_category"),
    path("category/edit_category/<int:id>/", views.edit_category, name="edit_category"),
    path("category/delete_category/<int:id>/", views.delete_category, name="delete_category"),
    
    path('brands/add_brand/', views.add_brand, name="add_brand"),
    path('brands/view_brand/', views.view_brand, name="view_brand"),
    path('brands/edit_brand/<int:id>', views.edit_brand, name="edit_brand"),
    path('brands/delete_brand/<int:id>', views.delete_brand, name="delete_brand"),
    
    path('brands/manageUser/', views.manageUser, name="manageUser"),
    
]