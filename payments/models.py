from django.db import models
from datetime import date
from django.conf import settings  # Importar settings para AUTH_USER_MODEL
from memberships.models import Membership

class Pago(models.Model):
    # Estado del pago
    ESTADOS = (
        (1, 'Pendiente'),
        (2, 'Completado'),
        (3, 'Fallido'),
    )
     # Método de pago
    METODOS_PAGO = [
        (1, 'Tarjeta de Crédito/Débito'),
        (2, 'PayPal'),
        (3, 'Transferencia Bancaria'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pagos')
    plan = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='pagos', null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    estado = models.PositiveSmallIntegerField(choices=ESTADOS, default=1)
    metodo_pago = models.PositiveSmallIntegerField(choices=METODOS_PAGO, default=1)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Pago {self.id} - {self.estado}'
