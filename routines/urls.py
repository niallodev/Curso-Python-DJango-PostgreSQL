from django.urls import path
from . import views

urlpatterns = [
    #! Admin
    path('routines_list', views.routines_list, name='routines_list'),
    path('create_routines/', views.create_routines, name='create_routines'),
    path('edit_routines/<int:rutina_id>/', views.edit_routines, name='edit_routines'),
    path('delete_routines/<int:rutina_id>/', views.delete_routines, name='delete_routines'),
    #! Entrenador
    path('routines_entreandor/<int:clase_id>/', views.routines_entrenador, name='routines_entrenador'),
    path('create_routines_entrenador/<int:clase_id>/', views.create_routines_entrenador, name='create_routines_entrenador'),
]