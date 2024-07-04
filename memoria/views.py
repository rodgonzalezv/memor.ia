from django.http import HttpResponse
from django.shortcuts import render

def inicio(request):
    context={}
    return render(request, 'web_inicio.html', context)

def quienes_somos(request):
    context={}
    return render(request, 'web_quienes_somos.html', context)

def planes(request):
    context={}
    return render(request, 'web_planes.html', context)

def galeria(request):
    context={}
    return render(request, 'web_galeria.html', context)

def contacto(request):
    context={}
    return render(request, 'web_contacto.html', context)