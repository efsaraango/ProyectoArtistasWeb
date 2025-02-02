import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import Artista
from .models import Obra



# Página de inicio
def index(request):
    obras = Obra.objects.all()
    return render(request, 'paginas/index.html', {'obras': obras})

# Página detalles de obra
def detalles_obra(request, id_obra):
    obra = get_object_or_404(Obra, id_obra=id_obra)
    artista = obra.id_artista
    return render(request, 'paginas/detalles_obra.html', {'obra': obra, 'artista': artista})






# Página de login de sesión
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')

        try:
            artista = Artista.objects.get(correo=correo)
            if not artista.is_approved:
                return render(request, 'paginas/login.html', {'error': 'Tu cuenta aún no ha sido aprobada.'})

            if artista and artista.check_password(contraseña):
                login(request, artista)
                return redirect('index') #
            else:
                raise ValueError("Credenciales incorrectas")
        except (ObjectDoesNotExist, ValueError):
            return render(request, 'paginas/login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'paginas/login.html')



# Página de perfil del usuario

def acceso(request, cedula=None):
    if cedula:  # Si se pasa la cédula, mostramos el perfil público de ese artista
        artista = get_object_or_404(Artista, cedula=cedula)
        es_propio_perfil = (request.user.is_authenticated and request.user.cedula == cedula)
    else:  # Si no se pasa cédula, asumimos que es el perfil del usuario logueado
        artista = get_object_or_404(Artista, correo=request.user.correo)
        es_propio_perfil = True

    obras = artista.artistas_obra.all()
    
    return render(request, 'paginas/acceso.html', {
        'artista': artista,
        'foto_base64': artista.foto_perfil if artista.foto_perfil else None,
        'obras': obras,
        'es_propio_perfil': es_propio_perfil
    })




# Página de subir obras
def subir_obras(request):
    usuario = request.user

    try:
        artista = Artista.objects.get(correo=usuario.correo)
    except Artista.DoesNotExist:
        return redirect('login')

    # Obtener la cantidad de obras actuales
    obras_actuales = artista.artistas_obra.count()
    limite_obras = artista.obtener_limite_obras()

    # Validar si el usuario ha alcanzado el límite
    if limite_obras is not None and obras_actuales >= limite_obras:
        return render(request, 'paginas/subir_obras.html', {
            'artista': artista,
            'foto_base64': artista.foto_perfil if artista.foto_perfil else None,
            'error': f"Has alcanzado el límite de {limite_obras} obras según tu plan.",
            'limite_obras': limite_obras  # Agregar el límite a la plantilla
        })

    if request.method == 'POST' and 'subir_obra' in request.POST:
        nombre_obra = request.POST.get('nombre_obra')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        ubicacion = request.POST.get('ubicacion')
        imagen = request.FILES.get('imagen')

        imagen_base64 = None
        if imagen:
            imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')

        Obra.objects.create(
            nombre_obra=nombre_obra,
            descripcion=descripcion,
            categoria=categoria,
            ubicacion=ubicacion,
            id_artista=artista,
            imagen=imagen_base64
        )
        return redirect('acceso')  # Redirigir a perfil tras subir obra

    return render(request, 'paginas/subir_obras.html', {
        'artista': artista,
        'foto_base64': artista.foto_perfil if artista.foto_perfil else None,
        'limite_obras': limite_obras  # Asegurar que se pasa a la plantilla
    })




@login_required
def cambiar_plan(request):
    usuario = request.user

    try:
        artista = Artista.objects.get(correo=usuario.correo)
    except Artista.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        nuevo_plan = request.POST.get('nuevo_plan')
        if nuevo_plan in Artista.PLANES_OBRAS:
            artista.categoriaplan = nuevo_plan
            artista.save()
            return redirect('subir_obras')  # Redirige a la página de subir obras después del cambio

    return render(request, 'paginas/cambiar_plan.html', {'artista': artista})




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




# Cerrar sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

