# classes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Clase, Reserva
from users.models import User
from .forms import ClaseForm, ReservaForm
from django.views.decorators.csrf import csrf_protect


# Vista para la lista de clases #!Admin
@login_required
def classes_list(request):
    classes = Clase.objects.all()  # Obtiene todos los usuarios
    return render(request, 'classes/classes_list.html', {'clases': classes, 'show_footer': True})

# Vista para la lista de clases #!Entrenador
@login_required
def classes_entrenador(request, user_id):
    classes = Clase.objects.filter(entrenador=user_id, is_active=True)  # Obtiene todos los usuarios
    
    return render(request, 'classes/classes_entrenador.html', {'clases': classes, 'show_footer': True})

# Vista para la lista de clases #!Miembros
@login_required
def classes_miembros(request):
    from django.db.models import Q
    user = request.user.id
    classes = Clase.objects.filter(is_active=True).exclude(
        id__in=Reserva.objects.filter(
            Q(usuario=user) & Q(is_active=True)  # Excluir reservas activas
        ).values('clase_id'))
    return render(request, 'classes/classes_miembros.html', {'clases': classes, 'show_footer': True})


# Vista para crear una nueva clase
@login_required
@csrf_protect
def create_classes(request):
    if request.method == 'POST':
        form = ClaseForm(request.POST)
        print("Esto es formulario")
        print(form)
        if form.is_valid():
            
            form.save()
            messages.success(request, "Clase creada con éxito.")
            return redirect('classes:classes_list')
    else:
        form = ClaseForm()
    return render(request, 'classes/create_classes.html', {'form': form})

# Vista para editar una clase existente
@login_required
def edit_classes(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    if request.method == 'POST':
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            form.save()
            messages.success(request, "Clase editada con éxito.")
            return redirect('classes:classes_list')
    else:
        form = ClaseForm(instance=clase)
    return render(request, 'classes/edit_classes.html', {'form': form})

# Vista para eliminar una clase
@login_required
def delete_classes(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    
    if request.method == 'POST':
        clase.is_active = False  # Aplicamos Eliminacion logica
        clase.save()
        messages.success(request, f"La clase {clase.nombre} ha sido eliminado correctamente.")
        return redirect('classes:classes_list')  # Cambia al nombre correcto de tu lista de usuarios
    return render(request, 'classes/delete_classes.html', {'clase': clase})
    

# Vista para la lista de reservas
@login_required
def classes_reserva(request, user_id, clase_id):
    
    user = request.user
    clase = get_object_or_404(Clase, id=clase_id)
    # Verificar si la reserva ya existe para este usuario y clase
    if not Reserva.objects.filter(usuario=user, clase=clase_id, is_active=True).exists():
        reserva = Reserva(usuario=user, clase=clase)
        reserva.save()  # Guardar la nueva reserva
        messages.success(request, f"Reserva creada para el usuario {user.username} para la clase {clase.nombre}")
    else:
        messages.success(request, "Ya existe una reserva para este usuario y clase.")
    return redirect('classes:classes_miembros')



# Vista para la lista de reservas #!Miembros
@login_required 
def reserve_list(request):
    user = request.user.id
    reservas = Reserva.objects.filter(usuario=user, is_active=True)

    return render(request, 'classes/reserva_list.html', {'reservas': reservas, 'show_footer': True})

# Vista para la lista de reservas #!Miembros
@login_required 
def reserve_delete(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    reserva.is_active = False  # Aplicamos Eliminacion logica
    reserva.save()
    messages.success(request, f"La reserva ha sido eliminado correctamente.")
    return redirect('classes:reserve_list')  # Cambia al nombre correcto de tu lista de usuarios

    
    
    
    # user = request.user.id
    # reservas = Reserva.objects.filter(usuario=user)

    # return render(request, 'classes/reserva_list.html', {'reservas': reservas, 'show_footer': True})





# Vista para crear una nueva reserva
@login_required
def create_reserve(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user  # Asigna el usuario al crear la reserva
            reserva.save()
            messages.success(request, "Reserva creada con éxito.")
            return redirect('classes:reserve_list')
    else:
        form = ReservaForm()
    return render(request, 'classes/reserva_register.html', {'form': form})

# Vista para editar una reserva existente
@login_required
def edit_reserve(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva editada con éxito.")
            return redirect('classes:reserve_list')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'classes/reserva_register.html', {'form': form})

# Vista para eliminar una reserva
@login_required
def delete_reserve(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.delete()
    messages.success(request, "Reserva eliminada con éxito.")
    return redirect('classes:reserve_list')


