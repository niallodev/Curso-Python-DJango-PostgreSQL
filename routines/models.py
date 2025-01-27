from django.db import models
from django.conf import settings
from classes.models import Clase  # Importar la clase para asociarla

class Rutina(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)  # Relación con la clase
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    frecuencia = models.CharField(max_length=50)  # Ej. "3 veces por semana"
    duracion_minutos = models.PositiveIntegerField()  # Duración en minutos
    fecha_inicio = models.DateField()  # Fecha de inicio de la rutina
    fecha_fin = models.DateField(null=True, blank=True)  # Fecha de fin de la rutina, opcional
    is_active = models.BooleanField(default=True)  # Si la rutina está activa o no

    def __str__(self):
        return f"Rutina de {self.clase.nombre} - {self.nombre}"