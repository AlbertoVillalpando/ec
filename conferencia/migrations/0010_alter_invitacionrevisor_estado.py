# Generated by Django 5.2.1 on 2025-05-23 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferencia', '0009_alter_invitacionrevisor_conferencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitacionrevisor',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'pendiente'), ('aceptado', 'aceptado'), ('rechazado', 'rechazado')], default='pendiente', max_length=10),
        ),
    ]
