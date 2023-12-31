from django.urls import include, path

from order import views

urlpatterns = [
    path('new/', views.new_order, name="new_order"),
    path('all/', views.get_orders, name="get_user_orders"),
    path('update/order_status/<int:id>/', views.process_order, name="process_order"),
    path('delete/<int:id>/', views.delete_order, name="delete_order"),
    path('confirm/<int:id>/', views.order_confirmation, name="confirm_order")
]
