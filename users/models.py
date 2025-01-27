from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from memberships.models import Membership 


class User(AbstractUser):
    USER_TYPES = (
        (1, 'Administrador'),
        (2, 'Entrenador'),
        (3, 'Miembro'),
    )
   
    # Campo para definir el tipo de usuario
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default=3)
    plan_membresia = models.ForeignKey(
        Membership,
        on_delete=models.SET_NULL,  # Si el plan es eliminado, el valor será NULL
        null=True,
        blank=True,
        related_name="users",  # Relación inversa desde Membership
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)


    # Campos conflictivos con related_name personalizado
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Evitar conflicto con el modelo auth.User
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Evitar conflicto con el modelo auth.User
        blank=True,
    )

    # Propiedad para facilitar la identificación del tipo de usuario
    @property
    def is_administrator(self):
        return self.user_type == 1

    @property
    def is_trainer(self):
        return self.user_type == 2

    @property
    def is_member(self):
        return self.user_type == 3

