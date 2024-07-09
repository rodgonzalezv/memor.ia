from django.shortcuts import render, get_object_or_404, redirect
from .forms import FamiliarForm, AdditionalImageForm
from memoria.models import Familiares, Comment, AdditionalImage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json, logging, os

logger = logging.getLogger(__name__)

@login_required
def carousel_home(request, pk):
    familiar = get_object_or_404(Familiares, id_familiar=pk)
    images = [familiar.avatar_picture.url] + [img.image.url for img in familiar.additional_images.all()]
    return render(request, 'carousel/index.html', {'familiar': familiar, 'images': images})

@login_required
def add_familiar(request):
    if request.method == 'POST':
        form = FamiliarForm(request.POST, request.FILES)
        if form.is_valid():
            familiar = form.save(commit=False)
            familiar.user = request.user

            if 'avatar_picture' in request.FILES:
                avatar_picture = request.FILES['avatar_picture']
                fs = default_storage
                path = fs.save('familiares_images/' + avatar_picture.name, ContentFile(avatar_picture.read()))
                familiar.avatar_picture = fs.url(path)

            familiar.save()
            return redirect('carousel:carousel_home', pk=familiar.id_familiar)
    else:
        form = FamiliarForm()
    return render(request, 'carousel/add_familiar.html', {'form': form})

@login_required
def edit_familiar(request, pk):
    familiar = get_object_or_404(Familiares, id_familiar=pk, user=request.user)
    if request.method == 'POST':
        form = FamiliarForm(request.POST, request.FILES, instance=familiar)
        if form.is_valid():
            if 'avatar_picture' in request.FILES:
                avatar_picture = request.FILES['avatar_picture']
                fs = default_storage
                path = fs.save('familiares_images/' + avatar_picture.name, ContentFile(avatar_picture.read()))
                familiar.avatar_picture = fs.url(path)
            form.save()
            return redirect('carousel:carousel_home', pk=familiar.id_familiar)
    else:
        form = FamiliarForm(instance=familiar)
    return render(request, 'carousel/edit_familiar.html', {'form': form})

@login_required
def remove_familiar(request, pk):
    familiar = get_object_or_404(Familiares, id_familiar=pk, user=request.user)
    if request.method == 'POST':
        familiar.delete()
        return redirect('dashboard:dashboard_home')
    return render(request, 'carousel/remove_familiar.html', {'familiar': familiar})


"""COMENTARIO DE PRUEBA"""


@csrf_exempt
@login_required
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image = request.FILES['image']
            familiar_id = request.POST['familiar_id']
            familiar = get_object_or_404(Familiares, id_familiar=familiar_id)

            additional_image = AdditionalImage(familiar=familiar, image=image)
            additional_image.save()

            return JsonResponse({'url': additional_image.image.url, 'familiar_id': familiar_id}, status=201)
        except KeyError as e:
            logger.error(f'Missing key: {str(e)}')
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def fetch_comments(request):
    image_url = request.GET.get('image_url')
    familiar_id = request.GET.get('familiar_id')
    comments = Comment.objects.filter(image_url=image_url, familiar_id=familiar_id).order_by('-created_at')
    comments_data = [{'username': comment.user.username, 'text': comment.text, 'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')} for comment in comments]
    return JsonResponse(comments_data, safe=False)

@csrf_exempt
@login_required
def post_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_url = data['image_url']
            text = data['text']
            familiar_id = data['familiar_id']
        except KeyError as e:
            logger.error(f'Missing key: {str(e)}')
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)

        try:
            familiar = get_object_or_404(Familiares, id_familiar=familiar_id)
        except Familiares.DoesNotExist:
            logger.error(f'Familiar with ID {familiar_id} does not exist')
            return JsonResponse({'error': f'Familiar with ID {familiar_id} does not exist'}, status=404)

        comment = Comment.objects.create(user=request.user, text=text, image_url=image_url, familiar=familiar)
        comment_data = {'username': comment.user.username, 'text': comment.text, 'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        return JsonResponse(comment_data, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
