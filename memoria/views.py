from django.http import HttpResponse
from django.shortcuts import render

def hola_mundo(request):
    return HttpResponse("Hola Mundo")

def simple(request, name):
    context = {'name':name}
    return render(request, 'simple.html', context)

def dinamico(request, name):
    context={'name':name}
    return render(request, 'simple.html', context)