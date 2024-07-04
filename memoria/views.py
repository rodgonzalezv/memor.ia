from django.http import HttpResponse
from django.shortcuts import render

def dinamico(request, name):
    arreglo=['josefina', 'matilda', 'javier','natalia']
    context={'name':name, 'nombres':arreglo}
    return render(request, 'web_inicio.html', context)