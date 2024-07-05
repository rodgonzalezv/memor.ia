from django.shortcuts import render, get_object_or_404, redirect
from .forms import FamiliarForm
from memoria.models import Familiares

def carousel_home(request, pk):
    familiar = get_object_or_404(Familiares, id_familiar=pk)
    # Assuming there is a way to get associated images with this familiar
    images = [familiar.avatar_picture]  # Add other images related to this familiar if any
    return render(request, 'carousel/index.html', {'familiar': familiar, 'images': images})

def add_familiar(request):
    if request.method == 'POST':
        form = FamiliarForm(request.POST, request.FILES)
        if form.is_valid():
            familiar = form.save(commit=False)
            familiar.user = request.user
            familiar.save()
            return redirect('carousel:carousel_home', familiar_id=familiar.id_familiar)
    else:
        form = FamiliarForm()
    return render(request, 'carousel/add_familiar.html', {'form': form})

def edit_familiar(request, pk):
    familiar = get_object_or_404(Familiares, id_familiar=pk, user=request.user)
    if request.method == 'POST':
        form = FamiliarForm(request.POST, request.FILES, instance=familiar)
        if form.is_valid():
            form.save()
            return redirect('carousel:carousel_home', familiar_id=familiar.id_familiar)
    else:
        form = FamiliarForm(instance=familiar)
    return render(request, 'carousel/edit_familiar.html', {'form': form})

def remove_familiar(request, pk):
    familiar = get_object_or_404(Familiares, id_familiar=pk, user=request.user)
    if request.method == 'POST':
        familiar.delete()
        return redirect('dashboard:dashboard_home')
    return render(request, 'carousel/remove_familiar.html', {'familiar': familiar})
