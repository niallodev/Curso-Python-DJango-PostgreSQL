from django import forms
from .models import Membership

class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['name', 'price', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de la Membresia'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio de la Membresia'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Breve descripcion'})
                
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''
    
   