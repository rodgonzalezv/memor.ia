from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .models import Planes
import requests
import os

def inicio(request):
    context={}
    return render(request, 'web_inicio.html', context)

def quienes_somos(request):
    context={}
    return render(request, 'web_quienes_somos.html', context)

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
    return render(request, 'web_planes.html', context)

def galeria(request):
    context={}
    return render(request, 'web_galeria.html', context)

def contacto(request):
    context={}
    return render(request, 'web_contacto.html', context)