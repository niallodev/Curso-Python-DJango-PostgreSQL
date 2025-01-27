from datetime import datetime
import pytz
from django.utils.timezone import make_aware
from django import forms
from .models import Clase, Reserva
from users.models import User 

class ClaseForm(forms.ModelForm):
    # Campo para seleccionar la fecha
    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',  # Selector de fecha nativo del navegador
                'placeholder': 'Seleccione la fecha'
            }
        )
    )
    class Meta:
        model = Clase
        fields = ['nombre', 'descripcion', 'entrenador', 'fecha', 'hora', 'cupo_maximo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de la Clase'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Descripcion de la Clase'})
        self.fields['entrenador'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seleccione el Entrenador'})
        self.fields['hora'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seleccione un Horario'})
        
        self.fields['cupo_maximo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cupo Máximo'})
        
        # Filtra los usuarios para que solo se muestren los entrenadores (is_staff=True)
        self.fields['entrenador'] = forms.ModelChoiceField(
            queryset=User.objects.filter(user_type=2),  # Solo los usuarios que son entrenadores
            empty_label="Seleccione un Entrenador",  # Etiqueta por defecto en el select
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione el Entrenador'}),
            to_field_name='id'  # Asegura que Django use el id para la validación.
        )
            
        # Campo para seleccionar la hora
        HORARIO_CHOICES=[
            ('09:00', '09:00 AM'),
            ('10:00', '10:00 AM'),
            ('11:00', '11:00 AM'),
            ('12:00', '12:00 PM'),
            ('13:00', '01:00 PM'),
            ('14:00', '02:00 PM'),
            ('15:00', '03:00 PM'),
            ('16:00', '04:00 PM'),
            ('17:00', '05:00 PM'),
        ]
        
        # Cambiar el campo de horario para que sea un select con opciones predefinidas
        self.fields['hora'] = forms.ChoiceField(
            choices=HORARIO_CHOICES,  # Utiliza las opciones de horario predefinidas
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        

      
        # Asegurarse de que 'cupo_maximo' sea un campo entero
        self.fields['cupo_maximo'] = forms.IntegerField(
            widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cupo Máximo'}),
            min_value=1,  # Por ejemplo, el cupo máximo no puede ser menor que 1
        )
        
        
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''
    
   
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['clase']
