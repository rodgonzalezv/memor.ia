from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from datetime import date
import random
import string
import os

class Memorial(models.Model):
    id_memorial=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=250)
    class Meta:
        verbose_name = ("Memorial")
        verbose_name_plural = ("Memorials")

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("Memorial_detail", kwargs={"pk": self.pk})

class Planes(models.Model):
    id_plan=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50)
    descripcion=models.TextField()
    cantidad = models.IntegerField()
    valor_factor = models.IntegerField()
    link_pago=models.CharField(max_length=50)
    class Meta:
        verbose_name = ("Planes")
        verbose_name_plural = ("Planes")

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("Planes_detail", kwargs={"pk": self.pk})

class Familiares(models.Model):
    OPC_NACIONALIDAD = (
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
        ('OT','Otra')
    )

    id_familiar = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_familiar = models.CharField(max_length=100)
    apellidos_familiar = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(auto_now=False, auto_now_add=False)
    fecha_deceso = models.DateField(auto_now=False, auto_now_add=False)
    parentezco = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=2, choices=OPC_NACIONALIDAD, default='CL')
    avatar_picture = models.ImageField(upload_to='familiares_images/', null=True, blank=True)
    unique_hash = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_familiar} {self.apellidos_familiar}"

    def save(self, *args, **kwargs):
        if not self.unique_hash:
            self.unique_hash = self.generate_unique_hash()
        super().save(*args, **kwargs)

    def generate_unique_hash(self):
        hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        while Familiares.objects.filter(unique_hash=hash).exists():
            hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return hash

class AdditionalImage(models.Model):
    image = models.ImageField(upload_to='additional_images/')
    familiar = models.ForeignKey(Familiares, on_delete=models.CASCADE, related_name='additional_images')

    def __str__(self):
        return f"Additional Image for {self.familiar.nombre_familiar}"

class Roles(models.Model):
    id_rol=models.AutoField(primary_key=True)
    nombre_rol=models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_rol

class Recuerdos(models.Model):
    id_recuerdo=models.AutoField(primary_key=True)
    nombre_recuerdo=models.CharField(max_length=100, default='Nombre Recuerdo')
    descripcion_recuerdo=models.TextField()

    def __str__(self):
        return self.nombre_recuerdo

class Usuarios(models.Model):
    id_usuario=models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email=models.EmailField()
    contraseña = models.CharField(max_length=128)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    
    def set_password(self, raw_password):
        self.contraseña = make_password(raw_password)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Usuarios_Planes(models.Model):
    id_plan_usuario=models.AutoField(primary_key=True)
    id_plan=models.ForeignKey(Planes, on_delete=models.CASCADE)
    id_usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    estado=models.IntegerField(default=0)
    fecha_act=models.DateField(auto_now_add=False, default=date.today)

    def __str__(self):
        return f"Usuario: {self.id_usuario.username} - Plan: {self.id_plan.nombre} - Estado: {self.estado}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    familiar = models.ForeignKey(Familiares, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.familiar.nombre_familiar}"
