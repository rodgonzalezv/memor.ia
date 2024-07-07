# carousel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FamiliarForm
from memoria.models import Familiares, Comment
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

def carousel_home(request, pk):
    familiar = get_object_or_404(Familiares, id_familiar=pk)
    images = [familiar.avatar_picture]
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

def fetch_comments(request):
    image_url = request.GET.get('image_url')
    comments = Comment.objects.filter(image_url=image_url).order_by('-created_at')
    comments_data = [{'username': comment.user.username, 'text': comment.text, 'created_at': comment.created_at} for comment in comments]
    return JsonResponse(comments_data, safe=False)

@csrf_exempt
def post_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_url = data['image_url']
        text = data['text']
        comment = Comment.objects.create(user=request.user, text=text, image_url=image_url)
        comment_data = {'username': comment.user.username, 'text': comment.text, 'created_at': comment.created_at}
        return JsonResponse(comment_data, status=201)