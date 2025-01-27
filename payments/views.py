# payments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Pago
from .forms import PagoForm
# from .forms import ClaseForm, ReservaForm
from django.views.decorators.csrf import csrf_protect


# Vista para la lista de clases
@login_required
def payments_list(request):
    pagos = Pago.objects.all()  # Obtiene todos los pagos
    print(pagos)
    return render(request, 'payments/payments_list.html', {'pagos': pagos, 'show_footer': True})

# Vista para editar un pago existente
@login_required
def edit_payments(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            messages.success(request, "Pago editado con éxito.")
            return redirect('payments:payments_list')
    else:
        form = PagoForm(instance=pago)
    return render(request, 'payments/edit_payments.html', {'form': form, 'pago':pago})

