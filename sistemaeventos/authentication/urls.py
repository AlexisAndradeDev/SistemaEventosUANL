from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
]