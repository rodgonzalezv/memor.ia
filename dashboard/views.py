from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from .models import Memorial, Planes, Usuarios_Planes, Familiares
import os
import requests
from .forms import formUserRegistro, formFamiliarRegistro, formFamiliarUpdate, CustomChangePasswordForm, UserProfileForm, SuscripcionForm

def userLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'dashboard_user_login.html', {'form': form})

def dashboard(request):
    context = {}
    return render(request, 'dashboard_home.html', context)


def dashboard(request):
    context={}
    return render(request, 'dashboard_home.html', context)

def login(request):
    context={}
    return render(request, 'dashboard_user_login.html', context)

def registro(request):
    context={}
    return render(request, 'dashboard_user_registro.html', context)

@login_required
def suscripcion(request):
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

    return render(request, 'dashboard_suscripcion.html', context)

def userLogout(request):
    logout(request)
    return redirect("userLogin")   


def userRegistro(request):
    if request.method == 'POST':
        form = formUserRegistro(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = Group.objects.get(name='Clientes')  
            user.groups.add(group)
            
            activation_link = 'http://localhost:8000/dashboard/activar-cuenta/' + str(user.id)
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
            return redirect('login')  
    else:
        form = formUserRegistro()
    return render(request, 'dashboard_user_registro.html', {'userRegistro': form})

User = get_user_model()
def activar_cuenta(request, user_id):
    try:
        user = User.objects.get(id=user_id, is_active=False)
        print(f"Usuario encontrado: {user.username}")
        # Activa la cuenta del usuario
        user.is_active = True
        user.save()
        print(f"Estado del usuario después de activar: {user.is_active}")
        return render(request, 'dashboard_cuenta_activada.html')
    except User.DoesNotExist:
        print("Usuario no encontrado o ya está activo.")
        return render(request, 'dashboard_error_activacion.html')