# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FamiliaresForm
from memoria.models import Familiares
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def dashboard_home(request):
    familiares = Familiares.objects.filter(user=request.user)
    return render(request, 'dashboard/dashboard_home.html', {'familiares': familiares})

@login_required
def list_familiares(request):
    familiares = Familiares.objects.filter(user=request.user)
    return render(request, 'dashboard/list_familiares.html', {'familiares': familiares})

@login_required
def add_familiar(request):
    if request.method == 'POST':
        form = FamiliaresForm(request.POST, request.FILES)
        if form.is_valid():
            familiar = form.save(commit=False)
            familiar.user = request.user
            familiar.save()
            return redirect('dashboard:list_familiares')
    else:
        form = FamiliaresForm()
    return render(request, 'dashboard/add_familiar.html', {'form': form})

@login_required
def update_familiar(request, pk):
    familiar = get_object_or_404(Familiares, pk=pk)
    if request.method == 'POST':
        form = FamiliaresForm(request.POST, request.FILES, instance=familiar)
        if form.is_valid():
            form.save()
            return redirect('dashboard:list_familiares')
    else:
        form = FamiliaresForm(instance=familiar)
    return render(request, 'dashboard/update_familiar.html', {'form': form})

@login_required
def delete_familiar(request, pk):
    familiar = get_object_or_404(Familiares, pk=pk)
    if request.method == 'POST':
        familiar.delete()
        return redirect('dashboard:list_familiares')
    return render(request, 'dashboard/delete_familiar.html', {'familiar': familiar})

def userLogout(request):
    logout(request)
    return redirect('/')   