# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, UserRegistrationAdminForm, UserEditForm, UserEditPerfileForm
from .models import User
from memberships.models import Membership
from payments.models import Pago
from django.views.decorators.csrf import csrf_protect


# Vista para el registro de usuarios
@csrf_protect
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Usuario activado por defecto
            user.save()
            messages.success(request, "Cuenta creada con éxito. Ahora puedes iniciar sesión.")
            return redirect('users:login')
        else:
            print(form.errors)  # Imprime los errores del formulario
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Vista para iniciar sesión
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)  # Aquí se inicia sesión
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('pages:index')  # Redirigir a la página de inicio después de iniciar sesión
            else:
                messages.error(request, "Tu cuenta está inactiva")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos")
    return render(request, 'users/login.html')

# Vista para cerrar sesión
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('users:login')

# Vista para registrar usuarios por parte del admin
def registerAdmin(request):
    if request.method == "POST":
        form = UserRegistrationAdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Usuario activado por defecto
            user.save()
            membresia = get_object_or_404(Membership, id=user.plan_membresia)
            # Crear un registro de pago basado en el plan de membresía seleccionado
            Pago.objects.create(
                usuario=user,
                fecha_pago=None,
                monto=membresia.price,
                estado=3,
                plan=user.plan_membresia,  # Asigna el plan desde el usuario
            )            
            messages.success(request, "Cuenta creada con éxito. Ahora puedes iniciar sesión.")
            return redirect('users:login')
        else:
            print(form.errors)
    else:
        form = UserRegistrationAdminForm()

    return render(request, 'users/user_register.html', {'form': form, 'show_footer': True})


# Vista para editar un usuario (solo el admin puede acceder)
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Obtiene el usuario o 404 si no existe
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Validamos si el usuario tiene un plan de membresía
            if user.plan_membresia:
                form.save()
                membresia = Membership.objects.filter(id=user.plan_membresia.id).first()
                # Crear un registro de pago basado en el plan de membresía seleccionado
                print("---------")
                print(membresia)
                if membresia:
                    Pago.objects.create(
                        usuario=user,
                        plan=membresia,
                        monto=membresia.price,  # Obtenemos el precio directamente
                        estado=1,  # Estado pendiente por defecto
                        metodo_pago=1,  # Método de pago predeterminado (Tarjeta)
                        descripcion=f'Pago por el plan {membresia.name}'
                    )
                messages.success(request, "Usuario actualizado con éxito.")
                return redirect('users:user_list')  # Redirige a la lista de usuarios después de editar
            else:
                messages.error(request, "Ingrese el tipo de membresia o plan")    
            
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user, 'show_footer': True})

# Vista para editar un usuario (solo el admin puede acceder)
@login_required
def edit_perfile(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Obtiene el usuario o 404 si no existe
    if request.method == "POST":
        form = UserEditPerfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado con éxito.")
            return redirect('pages:index')  # Redirige a la lista de usuarios después de editar
    else:
        form = UserEditPerfileForm(instance=user)
    return render(request, 'users/edit_perfile.html', {'form': form, 'user': user, 'show_footer': True})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.is_active = False  # Aplicamos Eliminacion logica
        user.save()
        messages.success(request, f"El usuario {user.username} ha sido eliminado correctamente.")
        return redirect('users:user_list')  # Cambia al nombre correcto de tu lista de usuarios

    return render(request, 'users/delete_user.html', {'user': user})


# Vista para ver la lista de usuarios
@login_required
def user_list(request):
    users = User.objects.all()  # Obtiene todos los usuarios
    return render(request, 'users/user_list.html', {'users': users, 'show_footer': True})

# Decorador de permisos para admins
def is_admin(user):
    return user.role == 'admin'

