# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from classes.models import Clase
from memberships.models import Membership 
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=15, required=False)
    # profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'plan_membresia']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese la contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita su contraseña'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Número de teléfono'})
        self.fields['plan_membresia'].queryset = Membership.objects.filter(is_active=True)  # Mostrar solo membresías activas
        self.fields['plan_membresia'].widget.attrs.update({'class': 'form-control'})
        # self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})
        
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''

class UserRegistrationAdminForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=15, required=False)
    
    # Añadir el campo para seleccionar el tipo de usuario (rol)
    user_type = forms.ChoiceField(
        choices=User.USER_TYPES,  # Opciones de roles definidas en el modelo
        widget=forms.Select,
        required=True,
        label="Tipo de Usuario"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'user_type', 'plan_membresia']
        # fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese la contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita su contraseña'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Número de teléfono'})
        self.fields['user_type'].widget.attrs.update({'class': 'form-control'})  # Aplicar clase al campo de tipo de usuario
        self.fields['plan_membresia'].queryset = Membership.objects.filter(is_active=True)  # Mostrar solo membresías activas
        self.fields['plan_membresia'].widget.attrs.update({'class': 'form-control'})
        
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=15, required=False)
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva Contraseña'}),
        label='Nueva Contraseña',
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Nueva Contraseña'}),
        label='Confirmar Nueva Contraseña',
        required=False
    )
    
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'profile_picture', 'plan_membresia']
        # Excluir el campo password que Django agrega por defecto
        # exclude = ['password']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombres Completos'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Apellidos Completos'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Número de teléfono'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})  # Aplicar clase al campo de tipo de usuario
        self.fields['plan_membresia'].queryset = Membership.objects.filter(is_active=True)  # Mostrar solo membresías activas
        self.fields['plan_membresia'].widget.attrs.update({'class': 'form-control'})

        
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''

    # Validar que la nueva contraseña y su confirmación coincidan
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Si se ha ingresado una nueva contraseña, validamos que ambas contraseñas coincidan
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    
    # Guardar los cambios y actualizar la contraseña si es necesario
    def save(self, commit=True):
        user = super().save(commit=False)

        # Obtener la nueva contraseña del formulario
        new_password = self.cleaned_data.get('new_password')

        # Si hay una nueva contraseña, se actualiza
        if new_password:
            user.set_password(new_password)

        # Guardar cambios si commit es True
        if commit:
            user.save()

class UserEditPerfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=15, required=False)
    # Campos de contraseña
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Actual'}),
        label='Contraseña Actual',
        required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva Contraseña'}),
        label='Nueva Contraseña',
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Nueva Contraseña'}),
        label='Confirmar Nueva Contraseña',
        required=False
    )
    
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clases CSS y placeholders a todos los campos
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombres Completos'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Apellidos Completos'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Número de teléfono'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})  # Aplicar clase al campo de tipo de usuario
        
        # Opcional: Elimina etiquetas (label) si las quieres vacías
        for field in self.fields.values():
            field.label = ''
            
    # # Método de validación para verificar la contraseña actual solo si se quiere cambiar
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        new_password = self.cleaned_data.get('new_password')

        # Si se ha ingresado una nueva contraseña, verifica la contraseña actual
        if new_password and not current_password:
            raise ValidationError("Debes ingresar tu contraseña actual para cambiarla.")
        
        # Si la contraseña actual se ingresa, validarla
        if current_password:
            user = self.instance  # El usuario que se está editando
            if not user.check_password(current_password):
                raise ValidationError("La contraseña actual no es correcta.")
        
        return current_password

    # Validar que la nueva contraseña y su confirmación coincidan
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Si se ha ingresado una nueva contraseña, validamos que ambas contraseñas coincidan
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    
     # Guardar los cambios y actualizar la contraseña si es necesario
    def save(self, commit=True):
        user = super().save(commit=False)

        # Obtener la nueva contraseña del formulario
        new_password = self.cleaned_data.get('new_password')

        # Si hay una nueva contraseña, se actualiza
        if new_password:
            user.set_password(new_password)

        # Guardar cambios si commit es True
        if commit:
            user.save()
