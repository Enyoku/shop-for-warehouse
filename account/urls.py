from django.urls import include, path

from account import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('me/', views.me, name='current_user_info'),
    path('update/', views.update_user, name='update_user'),
    path('delete/', views.delete_user, name='delete_user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password')
]
