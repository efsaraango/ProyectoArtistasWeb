# Generated by Django 3.2 on 2025-01-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artistas', '0002_auto_20250114_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artista',
            name='foto_perfil',
            field=models.TextField(blank=True, null=True),
        ),
    ]
