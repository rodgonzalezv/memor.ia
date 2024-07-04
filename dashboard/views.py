from django.shortcuts import render

def dashboard(request):
    context={}
    return render(request, 'dashboard_home.html', context)

def registro(request):
    context={}
    return render(request, 'dashboard_user_registro.html', context)