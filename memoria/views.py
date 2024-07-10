from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .models import Memorial, Planes, Usuarios_Planes, Familiares
import requests
import os
from .forms import formUserRegistro, formFamiliarRegistro, formFamiliarUpdate, CustomChangePasswordForm, UserProfileForm, SuscripcionForm

def hash_redirect(request, hash):
    try:
        # Buscar el familiar correspondiente al hash
        familiar = get_object_or_404(Familiares, unique_hash=hash)
        
        # Construir la URL completa para la redirección
        redirect_url = f"{settings.SITE_URL}/carousel/{familiar.id_familiar}/"
        
        # Redirigir a la URL específica del familiar
        return redirect(redirect_url)
    except Http404:
        # Devolver una respuesta con un script para mostrar un mensaje de alerta y redirigir
        message = "El memorial solicitado, no existe en nuestra base de datos, o corresponde a un memorial privado."
        script = f"""
        <script type="text/javascript">
            alert("{message}");
            window.location.href = "{settings.SITE_URL}/";
        </script>
        """
        return HttpResponse(script)


def home(request):

    return render(request, "memoria/home.html")

def quienes_somos(request):
    return render(request, "memoria/quienes_somos.html")

def planes(request):
    listaPlanes=Planes.objects.all()

    url = 'https://mindicador.cl/api'
    response = requests.get(url)
    data = response.json()
    dolar_value = data['dolar']['valor']
    uf_value = data['uf']['valor']
    bitcoin_value = data['bitcoin']['valor']
    context = {
        "planes": listaPlanes,
        "dolar": dolar_value,
        "uf": uf_value,
        "bitcoin": bitcoin_value
    }
    
    
    return render(request, "memoria/planes.html", context)

def galeria(request):
    return render(request, "memoria/galeria.html")

def contacto(request):
    return render(request, "memoria/contacto.html")

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:dashboard_home')  # Use the dashboard namespace here
        else:
            messages.error(request, 'Contraseña incorrecta')
            return render(request, 'memoria/userLogin.html')
    else:
        return render(request, 'memoria/userLogin.html')


    
def userLogout(request):
    logout(request)
    return redirect("userLogin")   
    
@login_required
def dashboard_home(request):
    return render(request, 'memoria/dashboard_home.html')

def userRegistro(request):
    if request.method == 'POST':
        form = formUserRegistro(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = Group.objects.get(name='Clientes')  
            user.groups.add(group)
            
            activation_link = 'http://localhost:8000/activar-cuenta/' + str(user.id)
            imagen_url = request.build_absolute_uri('https://virtual.cl/img/logo1.png')
            contenido_html = f"""
                <html>
                <head></head>
                <body>
                    <img src="{imagen_url}" style="width:200px"><br>
                    <h2>Bienvenido a MemorIA</h2>
                    <h2>{user.username.upper()}</h2><h3>
                    <a href="{activation_link}">Haz clic aquí para activar tu cuenta</a></h3>
                </body>
                </html>
            """
            send_mail(
                'Activa tu cuenta',
                '',
                'noreply@tu-sitio.com',
                [user.email],
                fail_silently=False,
                html_message=contenido_html
            )
            messages.success(request, 'Registro exitoso. Se ha enviado un correo electrónico para activar tu cuenta.')
            return redirect('dashboard_home')  
    else:
        form = formUserRegistro()
    return render(request, 'memoria/userRegistro.html', {'userRegistro': form})



User = get_user_model()
def activar_cuenta(request, user_id):
    try:
        user = User.objects.get(id=user_id, is_active=False)
        # Activa la cuenta del usuario
        user.is_active = True
        user.save()
        return render(request, 'memoria/cuenta_activada.html')
    except User.DoesNotExist:
        return render(request, 'memoria/error_activacion.html')
    

class CustomChangePasswordView(PasswordChangeView):
    form_class = CustomChangePasswordForm
    template_name = 'memoria/dashboard_pass.html'
    success_url = reverse_lazy('userLogout')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Contraseña cambiada correctamente.')
        logout(self.request)
        return response
    
@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'memoria/dashboard_perfil.html', {'form': form})
    
@login_required
def dashboard_suscripcion(request):
    user = request.user
    
    url = 'https://mindicador.cl/api'
    response = requests.get(url)
    data = response.json()
    uf_value = data['uf']['valor']

    suscripcion_existente = Usuarios_Planes.objects.filter(id_usuario=user.id).first()

    if suscripcion_existente:

        form = SuscripcionForm(request.POST or None, initial={'plan': suscripcion_existente.id_plan})
        if request.method == 'POST':
            if form.is_valid():
                suscripcion_existente.id_plan = form.cleaned_data['plan']
                suscripcion_existente.save()
                return redirect('dashboard_suscripcion')
    else:

        form = SuscripcionForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                plan = form.cleaned_data['plan']
                estado = 0
                Usuarios_Planes.objects.create(id_usuario=user, id_plan=plan, estado=estado)
                return redirect('dashboard_suscripcion')
    
    planes_asociados = Usuarios_Planes.objects.filter(id_usuario=user.id)
        
    context = {
        'form': form,
        'planes_asociados': planes_asociados,
        "uf": uf_value,
    }        

    return render(request, 'memoria/dashboard_suscripcion.html', context)

def familiarRegistro(request):
    if request.method == 'POST':
        form = formFamiliarRegistro(request.POST)
        if form.is_valid():
            names = form.cleaned_data['names']
            lastnames = form.cleaned_data['lastnames']
            date_of_birth = form.cleaned_data['date_of_birth']
            date_of_death = form.cleaned_data['date_of_death']
            relationship = form.cleaned_data['relationship']
            nationality = form.cleaned_data['nationality']
            if 'avatar_picture' in request.FILES:
                picture = request.FILES['avatar_picture']
                picture_path = os.path.join(settings.MEDIA_ROOT, picture.name)
                with open(picture_path, 'wb') as f:
                    for chunk in picture.chunks():
                        f.write(chunk)

            familiar = Familiares(
                nombre_familiar=names,
                apellidos_familiar=lastnames,
                fecha_nacimiento=date_of_birth,
                fecha_deceso=date_of_death,
                parentezco=relationship,
                nacionalidad=nationality,                
            )
            familiar.user_id=request.user.id
            familiar.save()
            #messages.success(request, 'Familiar creado exitosamente.')
            return redirect('dashboard_familiarListado')
            
            
    else:
        form = formFamiliarRegistro()
        form.fields['user_id'].initial = request.user.id
    
    context = {'form': form}
    return render(request, 'memoria/dashboard_familiarRegistro.html', context)

@login_required
def familiarListado(request):
    familiares = Familiares.objects.filter(user=request.user)
def suscripcion(request):
    usuario = request.user
    suscripcion = Usuarios_Planes.objects.filter(id_usuario=usuario).first()
    context = {
        'suscripcion': suscripcion
    }
    return render(request, 'suscripcion.html', context)
    # Create a list of dictionaries containing the desired information
    familiares_data = []
    for familiar in familiares:
        data = {
            'id_familiar':familiar.id_familiar,
            'nombre_apellidos': f'{familiar.nombre_familiar} {familiar.apellidos_familiar}',
            'edad': familiar.fecha_deceso.year - familiar.fecha_nacimiento.year,
            'parentezco': familiar.parentezco,
            'fecha_deceso': familiar.fecha_deceso,
        }
        familiares_data.append(data)

    context = {
        'familiares': familiares_data,
    }
    return render(request, 'memoria/dashboard_familiarListado.html', context)

@login_required
def familiarUpdate(request, familiar_id):
    familiar = get_object_or_404(Familiares, id_familiar=familiar_id, user=request.user)

    if request.method == 'POST':
        form = formFamiliarUpdate(request.POST, instance=familiar)
        if form.is_valid():
            form.save()
            return redirect('dashboard_familiarListado')
    else:
        form = formFamiliarUpdate(instance=familiar)

    context = {'form': form}
    return render(request, 'memoria/dashboard_familiarUpdate.html', context)


@login_required
def familiarDelete(request, familiar_id):
    familiar = get_object_or_404(Familiares, id_familiar=familiar_id, user=request.user)

    if request.method == 'POST':
        familiar.delete()
        #messages.success(request, 'Familiar eliminado exitosamente.')
        return redirect('dashboard_familiarListado')

    return render(request, 'memoria/dashboard_familiarListado.html', {'familiar': familiar})

def pago_exitoso(request):
    usuario_plan = Usuarios_Planes.objects.filter(id_usuario=request.user, estado=0).first()

    if usuario_plan:
        usuario_plan.estado = 1
        usuario_plan.save()

    return redirect('dashboard_suscripcion')


def queplan(request):
    usuario = request.user
    mensaje = ""
    nombre_plan = ""
    estado = ""
    fecha_activacion = ""

    try:
        registro = Usuarios_Planes.objects.get(id_usuario=usuario.id)
        estado = registro.estado
        fecha_activacion = registro.fecha_activacion

        if estado == 0:
            mensaje = "Tienes una suscripción elegida, pero no la has activado."
        elif estado == 1:
            mensaje = "Esta es tu suscripción."
            plan = registro.id_plan
            nombre_plan = plan.nombre

    except Usuarios_Planes.DoesNotExist:
        mensaje = "No tienes ninguna suscripción elegida."

    context = {
        'mensaje': mensaje,
        'nombre_plan': nombre_plan,
        'estado': estado,
        'fecha_activacion': fecha_activacion
    }

    return render(request, 'memoria/dashboard_base.html', context)