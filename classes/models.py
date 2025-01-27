from django.db import models
from datetime import date
from django.conf import settings  # Importar settings para AUTH_USER_MODEL

class Clase(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    entrenador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    hora = models.CharField(max_length=5)
    cupo_maximo = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="reservas")
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Reserva de {self.usuario.username} en {self.clase.nombre}"
