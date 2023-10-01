from django.urls import path, include

from order import views


urlpatterns = [
    path('new/', views.new_order, name="new_order"),
]
