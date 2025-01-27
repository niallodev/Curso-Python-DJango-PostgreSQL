from django.urls import path
from . import views

urlpatterns = [
    # memberships
    path('memberships_list', views.memberships_list, name='memberships_list'),
    path('create_memberships/', views.create_memberships, name='create_memberships'),
    path('edit_memberships/<int:membresia_id>/', views.edit_memberships, name='edit_memberships'),
    path('delete_memberships/<int:membresia_id>/', views.delete_memberships, name='delete_memberships'),
    #!Miembro
    path('memberships_user/<int:user_id>/', views.memberships_user, name='memberships_user'),
    
]