from django import forms
from memoria.models import Familiares
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput
from django.forms import PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class FamiliaresForm(forms.ModelForm):
    class Meta:
        model = Familiares
        fields = ['nombre_familiar', 'apellidos_familiar', 'fecha_nacimiento', 'fecha_deceso', 'parentezco', 'nacionalidad', 'avatar_picture']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_deceso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre_familiar': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos_familiar': forms.TextInput(attrs={'class': 'form-control'}),
            'parentezco': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'avatar_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


        
class UserProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(render_value=False)
    
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', 'Guardar perfil'))

    class Meta:
        model = UserModel
        fields = ['username','first_name', 'last_name']

class CustomChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Cambiar Contraseña'))
   