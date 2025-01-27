from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago', 'estado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['metodo_pago'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio de la Membresia'})
        self.fields['estado'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Breve descripcion'})
                
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''
    
   