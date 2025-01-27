from django.urls import path
from . import views

urlpatterns = [
    # clases #!Admin
    path('classes_list', views.classes_list, name='classes_list'),
    path('create_classes/', views.create_classes, name='create_classes'),
    path('edit_classes/<int:clase_id>/', views.edit_classes, name='edit_classes'),
    path('delete_classes/<int:clase_id>/', views.delete_classes, name='delete_classes'),
   #Clases #!Entrenador
   path('classes_entrenador/<int:user_id>/', views.classes_entrenador, name='classes_entrenador'),
    #Clases #!Miembros
    path('classes_miembros/', views.classes_miembros, name='classes_miembros'),
    path('classes_reserva/<int:user_id>/<int:clase_id>/', views.classes_reserva, name='classes_reserva'),
    path('reserve_list/', views.reserve_list, name='reserve_list'),
    path('reserve_delete/<int:reserva_id>', views.reserve_delete, name='reserve_delete'),
   
   
    # reserva
    path('reserve_list', views.reserve_list, name='reserve_list'),
    path('create_reserve/', views.create_reserve, name='create_reserve'),
    path('edit_reserve/<int:user_id>/', views.edit_reserve, name='edit_reserve'),
    path('delete_reserve/<int:user_id>/', views.delete_reserve, name='delete_reserve'),
    
]
