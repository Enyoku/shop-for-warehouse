from django.urls import path

from product import views

urlpatterns = [
    path('category/new/', views.create_new_category, name='create_category'),
    path('category/', views.get_all_categories, name='create_category'),
    path('products/', views.get_all_products, name='products'),
    path('products/<int:id>/', views.get_product, name='get_product'),
    path('products/<int:id>/update/', views.update_product_credentials, name='get_product'),
    path('products/<int:id>/delete/', views.delete_product, name='get_product'),
    path('products/new/', views.new_product, name='new_product')
]
