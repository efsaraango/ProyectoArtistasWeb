# Generated by Django 3.2 on 2025-01-22 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artistas', '0006_auto_20250122_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artista',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Aprobado por administrador'),
        ),
    ]
