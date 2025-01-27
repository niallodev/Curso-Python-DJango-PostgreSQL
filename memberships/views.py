# memberships/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Membership
from .forms import MembresiaForm
from django.views.decorators.csrf import csrf_protect


# Vista para la lista de membresia
@login_required
def memberships_list(request):
    membresia = Membership.objects.all() 
    return render(request, 'memberships/memberships_list.html', {'membresias': membresia, 'show_footer': True})

# Vista para la membresia
@login_required
def memberships_user(request, user_id):
    print("--------------")
    print(user_id)
    
    membresia = Membership.objects.filter(id=user_id) 
    
    return render(request, 'memberships/memberships_user.html', {'membresia': membresia, 'show_footer': True})


# Vista para crear una nueva membresia
@login_required
@csrf_protect
def create_memberships(request):
    if request.method == 'POST':
        form = MembresiaForm(request.POST)
        if form.is_valid():
            memberships = form.save(commit=False)
            memberships.is_active = True  # Usuario activado por defecto
            memberships.save()
            messages.success(request, "Membresia creada con éxito.")
            return redirect('memberships:memberships_list')
    else:
        form = MembresiaForm()
    return render(request, 'memberships/create_memberships.html', {'form': form})

# Vista para editar una membresia existente
@login_required
def edit_memberships(request, membresia_id):
    membresia = get_object_or_404(Membership, id=membresia_id)
    if request.method == 'POST':
        form = MembresiaForm(request.POST, instance=membresia)
        if form.is_valid():
            form.save()
            messages.success(request, "Membresia editada con éxito.")
            return redirect('memberships:memberships_list')
    else:
        form = MembresiaForm(instance=membresia)
    return render(request, 'memberships/edit_memberships.html', {'form': form})

# Vista para eliminar una membresia
@login_required
def delete_memberships(request, membresia_id):
    membresia = get_object_or_404(Membership, id=membresia_id)
    
    if request.method == 'POST':
        membresia.is_active = False  # Aplicamos Eliminacion logica
        membresia.save()
        messages.success(request, f"La Membresia {membresia.name} ha sido eliminado correctamente.")
        return redirect('memberships:memberships_list')  # Cambia al nombre correcto de tu lista de usuarios

    return render(request, 'memberships/delete_memberships.html', {'membresia': membresia})
    

