from datetime import datetime
import pytz
from django.utils.timezone import make_aware
from django import forms
from .models import Rutina
from classes.models import Clase 

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['clase', 'nombre', 'descripcion', 'frecuencia', 'duracion_minutos', 'fecha_inicio', 'fecha_fin']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['clase'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de la Rutina'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Una Breve Descripción'})
        self.fields['frecuencia'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seleccione la Fecuencia'})
        self.fields['duracion_minutos'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seleccione la Duración'})
        self.fields['fecha_inicio'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Fecha de Inicio', 'type': 'date'}
        )
        self.fields['fecha_fin'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Fecha de Fin', 'type': 'date'}
        )       
        
        # Filtra los usuarios para que solo se muestren los entrenadores (is_staff=True)
        self.fields['clase'] = forms.ModelChoiceField(
            queryset=Clase.objects.all(),  # Solo los usuarios que son entrenadores
            empty_label="Seleccione una Clase",  # Etiqueta por defecto en el select
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione el Entrenador'}),
            to_field_name='id'  # Asegura que Django use el id para la validación.
        )
            
        # Campo para seleccionar la hora
        FRECUENCIA_CHOICES=[
            (1, '1 vez por semana'),
            (2, '2 veces port semana'),
            (3, '3 veces port semana'),
            (4, '4 veces por semana'),
            (5, '5 veces por semana'),
            (6, '6 veces por semana'),
    
        ]
        
        # Cambiar el campo de horario para que sea un select con opciones predefinidas
        self.fields['frecuencia'] = forms.ChoiceField(
            choices=FRECUENCIA_CHOICES,  # Utiliza las opciones de horario predefinidas
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        

      
        
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''
         # Añadir etiquetas a los campos de fecha para que el usuario sepa cuál es cuál
        self.fields['fecha_inicio'].label = 'Fecha de Inicio'  # Etiqueta explícita para el campo de inicio
        self.fields['fecha_fin'].label = 'Fecha de Fin'  # Etiqueta explícita para el campo de fin
    
   
class RutinaEntrenadorForm(forms.ModelForm):
   

    class Meta:
        model = Rutina
        fields = ['clase', 'nombre', 'descripcion', 'frecuencia', 'duracion_minutos', 'fecha_inicio', 'fecha_fin']
    
    def __init__(self, *args, clase_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        print("tenemos el id de clase", clase_id)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['clase'].widget.attrs.update({'class': 'form-control', 'disabled': 'true'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de la Rutina'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Una Breve Descripción'})
        self.fields['frecuencia'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seleccione la Fecuencia'})
        self.fields['duracion_minutos'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seleccione la Duración'})
        self.fields['fecha_inicio'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Fecha de Inicio', 'type': 'date'}
        )
        self.fields['fecha_fin'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Fecha de Fin', 'type': 'date'}
        )       
        
        # Filtra los usuarios para que solo se muestren los entrenadores (is_staff=True)
        self.fields['clase'] = forms.ModelChoiceField(
            queryset=Clase.objects.all(),  # Solo los usuarios que son entrenadores
            empty_label="Seleccione una Clase",  # Etiqueta por defecto en el select
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione el Entrenador'}),
            to_field_name='id'  # Asegura que Django use el id para la validación.
        )
            
        # Campo para seleccionar la hora
        FRECUENCIA_CHOICES=[
            (1, '1 vez por semana'),
            (2, '2 veces port semana'),
            (3, '3 veces port semana'),
            (4, '4 veces por semana'),
            (5, '5 veces por semana'),
            (6, '6 veces por semana'),
    
        ]
        
        # Cambiar el campo de horario para que sea un select con opciones predefinidas
        self.fields['frecuencia'] = forms.ChoiceField(
            choices=FRECUENCIA_CHOICES,  # Utiliza las opciones de horario predefinidas
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''
         # Añadir etiquetas a los campos de fecha para que el usuario sepa cuál es cuál
        self.fields['fecha_inicio'].label = 'Fecha de Inicio'  # Etiqueta explícita para el campo de inicio
        self.fields['fecha_fin'].label = 'Fecha de Fin'  # Etiqueta explícita para el campo de fin
        if clase_id:
            # Configura el campo clase
            self.fields['clase'].initial = clase_id  # Asigna el valor inicial del campo
            self.fields['clase'].disabled = True  # Desactívalo para que sea solo de lectura
        
    def clean(self):
        cleaned_data = super().clean()
        # Evitar cambios en el campo 'clase'
        if 'clase' in self.initial:
            cleaned_data['clase'] = self.initial['clase']
        return cleaned_data
    
   