from django.urls import path
from . import views

urlpatterns = [
    # pagos
    path('payments_list', views.payments_list, name='payments_list'),
    path('edit_payments/<int:pago_id>/', views.edit_payments, name='edit_payments'),
]
