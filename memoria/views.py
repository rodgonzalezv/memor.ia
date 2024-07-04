from django.http import HttpResponse
from django.shortcuts import render

def hola_mundo(request):
    return HttpResponse("Hola Mundo")

def simple(request):
    return render(request, 'simple.html', {})