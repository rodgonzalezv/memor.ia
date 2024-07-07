from django import forms
from memoria.models import Familiares

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
