from django.urls import include, path

from account import views

urlpatterns = [
    path('register/', views.register, name='register'),
]
