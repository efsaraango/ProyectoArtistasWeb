# Generated by Django 3.2 on 2025-01-29 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artistas', '0007_alter_artista_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artista',
            name='categoriaplan',
            field=models.CharField(choices=[('planGratis', 'Gratis'), ('planBasico', 'Plan Básico'), ('planPremium', 'Plan Premium')], max_length=50, null=True),
        ),
    ]
