# routines/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Rutina
from classes.models import Clase

from .forms import RutinaForm, RutinaEntrenadorForm
from django.views.decorators.csrf import csrf_protect


# Vista para la lista de rutinas
@login_required
def routines_list(request):
    routines = Rutina.objects.all()  # Obtiene todos los usuarios
    return render(request, 'routines/routines_list.html', {'rutinas': routines, 'show_footer': True})

# Vista para la lista de rutinas del entrenador
@login_required
def routines_entrenador(request, clase_id ):
    routines = Rutina.objects.filter(clase=clase_id, is_active=True)  # Obtiene todos las rutinas de la clase
    clase_id = Clase.objects.get(id=clase_id)
    # print("clase_id",clase_id.id)
    return render(request, 'routines/routines_entrenador.html', {'rutinas': routines, 'clase_id':clase_id.id, 'user_id':clase_id.entrenador.id, 'show_footer': True})


# Vista para crear una nueva rutina
@login_required
@csrf_protect
def create_routines(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            routines = form.save(commit=False)
            routines.is_active = True  # Usuario activado por defecto
            routines.save()
            messages.success(request, "Rutina creada con éxito.")
            return redirect('routines:routines_list')
    else:
        form = RutinaForm()
    return render(request, 'routines/create_routines.html', {'form': form})


# Vista para crear una nueva rutina

@login_required
@csrf_protect
def create_routines_entrenador(request, clase_id):
    if request.method == 'POST':
        
        form = RutinaEntrenadorForm(request.POST, clase_id=clase_id)
        if form.is_valid():
            routines = form.save(commit=False)
            routines.is_active = True
            routines.save()
            messages.success(request, "Rutina creada con éxito.")
            return redirect('routines:routines_entrenador', clase_id=clase_id)
    else:
        form = RutinaEntrenadorForm(clase_id=clase_id)
    return render(request, 'routines/create_routines_entrenador.html', {'form': form, 'clase_id':clase_id})

# Vista para editar una rutina existente
@login_required
def edit_routines(request, rutina_id):
    rutina = get_object_or_404(Rutina, id=rutina_id)
    if request.method == 'POST':
        form = RutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, "Rutina editada con éxito.")
            return redirect('routines:routines_list')
    else:
        form = RutinaForm(instance=rutina)
    return render(request, 'routines/edit_routines.html', {'form': form})

# Vista para eliminar una rutina
@login_required
def delete_routines(request, rutina_id):
    rutina = get_object_or_404(Rutina, id=rutina_id)
    
    if request.method == 'POST':
        rutina.is_active = False  # Aplicamos Eliminacion logica
        rutina.save()
        messages.success(request, f"La Rutina {rutina.nombre} ha sido eliminado correctamente.")
        return redirect('routines:routines_list')  # Cambia al nombre correcto de tu lista de usuarios

    return render(request, 'routines/delete_routines.html', {'rutina': rutina})
   