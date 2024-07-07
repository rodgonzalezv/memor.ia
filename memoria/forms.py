from django import forms
from django.forms.widgets import DateInput
from django.forms import PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from .models import Planes
from .models import Familiares
from .models import Comment
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class formUserRegistro(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-control'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrarse como Usuario'))

class CustomChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Cambiar Contraseña'))
        
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
        
        
class SuscripcionForm(forms.Form):
    plan = forms.ModelChoiceField(queryset=Planes.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit();'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].label_from_instance = lambda obj: obj.nombre
        self.fields['plan'].widget.attrs.update({'class': 'form-control'})

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

NATIONALITIES = (
    ('AR', 'Argentina'),
    ('BO', 'Bolivia'),
    ('BR', 'Brasil'),
    ('CL', 'Chile'),
    ('CO', 'Colombia'),
    ('CR', 'Costa Rica'),
    ('CU', 'Cuba'),
    ('EC', 'Ecuador'),
    ('SV', 'El Salvador'),
    ('GT', 'Guatemala'),
    ('HN', 'Honduras'),
    ('MX', 'México'),
    ('NI', 'Nicaragua'),
    ('PA', 'Panamá'),
    ('PY', 'Paraguay'),
    ('PE', 'Perú'),
    ('PR', 'Puerto Rico'),
    ('DO', 'República Dominicana'),
    ('UY', 'Uruguay'),
    ('VE', 'Venezuela'),
    ('OT', 'Otra'),
)

class formFamiliarRegistro(forms.Form):
    names = forms.CharField(max_length=50, label='Nombres', widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastnames = forms.CharField(max_length=50, label='Apellidos', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(
        label='Fecha de nacimiento',
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_of_death = forms.DateField(
        label='Fecha de deceso',
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    relationship = forms.CharField(max_length=100, label='Parentezco / Relación', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nationality = forms.ChoiceField(choices=NATIONALITIES, label='Nacionalidad', widget=forms.Select(attrs={'class': 'form-control'}))
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    ##picture = forms.ImageField(label='Imagen')

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        date_of_death = cleaned_data.get('date_of_death')

        if date_of_birth and date_of_death:
            if date_of_birth >= date_of_death:
                raise ValidationError("La fecha de nacimiento debe ser anterior a la fecha de deceso.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-control'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar'))


class formFamiliarUpdate(forms.ModelForm):
    class Meta:
        model = Familiares
        fields = ['nombre_familiar', 'apellidos_familiar', 'fecha_nacimiento', 'fecha_deceso', 'parentezco', 'nacionalidad']
        labels = {
            'nombre_familiar': 'Nombres',
            'apellidos_familiar': 'Apellidos',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'fecha_deceso': 'Fecha de deceso',
            'parentezco': 'Parentezco / Relación',
            'nacionalidad': 'Nacionalidad',
        }
        widgets = {
            'nombre_familiar': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos_familiar': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_deceso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'parentezco': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')
        fecha_deceso = cleaned_data.get('fecha_deceso')

        if fecha_nacimiento and fecha_deceso and fecha_deceso < fecha_nacimiento:
            raise ValidationError("La fecha de deceso debe ser posterior a la fecha de nacimiento.")

        return cleaned_data
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add a comment', 'rows': 3}),
        }