from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class ArtistaManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo electrónico es obligatorio")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)  # Encripta la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(correo, password, **extra_fields)

class Artista(AbstractBaseUser, PermissionsMixin):
    cedula = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(null=True, blank=True)
    categoria = models.CharField(max_length=50, null=True, choices=[
        ('grafiti', 'Grafiti'),
        ('escultura', 'Escultura'),
        ('fotografia', 'Fotografía'),
    ])
    correo = models.EmailField(unique=True)
    categoriaplan = models.CharField(max_length=50, null=True, choices=[
        ('planBasico', 'Plan Básico'),
        ('planPremiun', 'Plan Premium'),
    ])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    foto_perfil = models.TextField(null=True, blank=True)  # Para almacenar base64


    # Campo para login
    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre", "apellido"]

    # Manager personalizado
    objects = ArtistaManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"