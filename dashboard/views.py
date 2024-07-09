# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FamiliaresForm
from memoria.models import Familiares
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import UserProfileForm, CustomChangePasswordForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
import qrcode
from django.conf import settings


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

            # Generar código QR
            qr_url = f"{settings.SITE_URL}/{familiar.unique_hash}"
            qr = qrcode.make(qr_url)
            qr_filename = os.path.join(settings.MEDIA_ROOT, 'qrcodes', f'{familiar.unique_hash}.png')
            qr.save(qr_filename)

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



@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'dashboard/user_profile.html', {'form': form})





class CustomChangePasswordView(PasswordChangeView):
    form_class = CustomChangePasswordForm
    template_name = 'dashboard/dashboard_pass.html'
    success_url = reverse_lazy('userLogout')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Contraseña cambiada correctamente.')
        logout(self.request)
        return response