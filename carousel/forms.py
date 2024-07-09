from django import forms
from memoria.models import Familiares, AdditionalImage

class FamiliarForm(forms.ModelForm):
    class Meta:
        model = Familiares
        fields = ['nombre_familiar', 'apellidos_familiar', 'fecha_nacimiento', 'fecha_deceso', 'parentezco', 'nacionalidad', 'avatar_picture']

class AdditionalImageForm(forms.ModelForm):
    class Meta:
        model = AdditionalImage
        fields = ['image']