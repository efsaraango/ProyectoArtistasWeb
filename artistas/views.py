import base64
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Artista
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

# Página de inicio
def index(request):
    return render(request, 'paginas/index.html')

# Página de inicio de sesión

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')

        try:
            # Buscar el usuario personalizado
            artista = Artista.objects.get(correo=correo)
            if artista and artista.check_password(contraseña):  # Verifica la contraseña
                login(request, artista)  # Inicia sesión
                return redirect('acceso')
            else:
                raise ValueError("Credenciales incorrectas")
        except (ObjectDoesNotExist, ValueError):
            # Si no encuentra al usuario o las credenciales fallan
            return render(request, 'paginas/login.html', {'error': 'Credenciales incorrectas'})

    # Si es GET, muestra el formulario de login
    return render(request, 'paginas/login.html')


# Página de acceso después del login
@login_required
def acceso(request):
    usuario = request.user

    try:
        artista = Artista.objects.get(correo=usuario.correo)
    except Artista.DoesNotExist:
        return render(request, 'paginas/acceso.html', {'error': 'Usuario no encontrado.'})

    if request.method == 'POST':
        artista.nombre = request.POST.get('nombre')
        artista.apellido = request.POST.get('apellido')
        artista.correo = request.POST.get('correo')

        # Manejar la actualización de la imagen
        if request.FILES.get('foto_perfil'):
            artista.foto_perfil = base64.b64encode(request.FILES['foto_perfil'].read()).decode('utf-8')

        artista.save()
        return redirect('acceso')

    # Convertir la foto de perfil a base64 para mostrarla
    foto_base64 = artista.foto_perfil if artista.foto_perfil else None

    return render(request, 'paginas/acceso.html', {
        'artista': artista,
        'foto_base64': foto_base64,
    })





# Página de registro
def registro(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        edad = request.POST.get('edad')
        categoria = request.POST.get('categoria')
        correo = request.POST.get('correo')
        categoriaplan = request.POST.get('categoriaplan')
        contraseña = request.POST.get('contraseña')
        foto_perfil = request.FILES.get('foto_perfil')

        try:
            # Leer la imagen como binario si se subió
            foto_perfil_data = None
            if foto_perfil:
                foto_perfil_data = base64.b64encode(foto_perfil.read()).decode('utf-8')

            # Crear el objeto Artista con la imagen binaria
            artista = Artista.objects.create(
                cedula=cedula,
                nombre=nombre,
                apellido=apellido,
                edad=edad,
                categoria=categoria,
                correo=correo,
                categoriaplan=categoriaplan,
                password=make_password(contraseña),
                foto_perfil=foto_perfil_data  # Almacena la imagen como binario
            )
            return render(request, 'paginas/registro.html', {
                'mensaje': 'Registro exitoso',
                'tipo': 'success'
            })
        except Exception as e:
            return render(request, 'paginas/registro.html', {
                'mensaje': f'Error al registrar el artista: {e}',
                'tipo': 'error'
            })

    return render(request, 'paginas/registro.html')




# Mostrar artistas
def mostrar_artistas(request):
    artistas = Artista.objects.all()

    artistas_con_imagenes = []
    for artista in artistas:
        try:
            foto_base64 = artista.foto_perfil if artista.foto_perfil else None
        except Exception:
            foto_base64 = None  # Si hay algún problema, omitir la imagen
        
        artistas_con_imagenes.append({
            'nombre': artista.nombre,
            'apellido': artista.apellido,
            'cedula': artista.cedula,
            'categoria': artista.categoria,
            'correo': artista.correo,
            'categoriaplan': artista.categoriaplan,
            'foto_base64': foto_base64,
        })

    return render(request, 'paginas/mostrar.html', {'artistas': artistas_con_imagenes})


# Cerrar sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def edit_perfil(request):
    usuario = request.user

    try:
        artista = Artista.objects.get(correo=usuario.correo)
    except Artista.DoesNotExist:
        return render(request, 'paginas/editperfil.html', {'error': 'Usuario no encontrado.'})

    if request.method == 'POST':
        artista.nombre = request.POST.get('nombre', artista.nombre)
        artista.apellido = request.POST.get('apellido', artista.apellido)
        artista.correo = request.POST.get('correo', artista.correo)

        # Manejar la actualización de la imagen (opcional)
        if request.FILES.get('foto_perfil'):
            foto_file = request.FILES['foto_perfil']
            artista.foto_perfil = base64.b64encode(foto_file.read()).decode('utf-8')

        artista.save()
        return redirect('edit_perfil')

    # Decodificar la foto a base64 para mostrarla
    foto_base64 = None
    if artista.foto_perfil:
        foto_base64 = artista.foto_perfil  # Ya está en base64

    return render(request, 'paginas/editperfil.html', {
        'artista': artista,
        'foto_base64': foto_base64,
    })
  
