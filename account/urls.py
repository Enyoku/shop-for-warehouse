from django.urls import include, path

from account import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('me/', views.me, name='current_user_info'),
    path('update/', views.update_user, name='update_user'),
    path('delete/', views.delete_user, name='delete_user')
]
