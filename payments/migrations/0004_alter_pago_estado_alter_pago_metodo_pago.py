# Generated by Django 5.1.5 on 2025-01-26 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_pago_estado_alter_pago_metodo_pago_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='estado',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pendiente'), (2, 'Completado'), (3, 'Fallido')], default=1),
        ),
        migrations.AlterField(
            model_name='pago',
            name='metodo_pago',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Tarjeta de Crédito/Débito'), (2, 'PayPal'), (3, 'Transferencia Bancaria')]),
        ),
    ]
