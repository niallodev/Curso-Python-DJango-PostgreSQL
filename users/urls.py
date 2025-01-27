# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),  # Lista de usuarios
    path('register/', views.register, name='register'), # Registro de Usuario desde afuera
    path('user_register/', views.registerAdmin, name='user_register'), # Registro de Usuario por un admin
    path('login/', views.login_view, name='login'), # Inicio de Sesion
    path('logout/', views.logout_view, name='logout'), # Cierre de Sesion
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),  #Editar un usuario
    path('edit_perfile/<int:user_id>/', views.edit_perfile, name='edit_perfile'),  #Editar un usuario
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),  #Editar un usuario
        
]
