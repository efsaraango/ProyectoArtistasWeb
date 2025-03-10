# Generated by Django 5.1.4 on 2025-01-09 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artista',
            fields=[
                ('cedula', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('edad', models.PositiveIntegerField(null=True)),
                ('categoria', models.CharField(choices=[('grafiti', 'Grafiti'), ('escultura', 'Escultura'), ('fotografia', 'Fotografía')], max_length=50, null=True)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('categoriaplan', models.CharField(choices=[('planBasico', 'Plan Básico'), ('planPremiun', 'Plan Premium')], max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('password', models.CharField(max_length=128)),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='fotos_perfil/')),
            ],
        ),
    ]
