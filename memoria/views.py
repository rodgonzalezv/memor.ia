from django.http import HttpResponse
from django.shortcuts import render

def inicio(request):
    context={}
    return render(request, 'web_inicio.html', context)