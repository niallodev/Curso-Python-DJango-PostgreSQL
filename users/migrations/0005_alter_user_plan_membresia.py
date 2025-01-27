# Generated by Django 5.1.5 on 2025-01-26 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_plan_membresia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='plan_membresia',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Plan Básico'), (2, 'Plan Premium'), (3, 'Plan VIP')], default=1),
        ),
    ]
