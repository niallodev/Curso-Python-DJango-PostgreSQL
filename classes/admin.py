from django.contrib import admin
from .models import Clase, Reserva

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'entrenador', 'fecha', 'hora', 'cupo_maximo')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'clase', 'fecha_reserva')
