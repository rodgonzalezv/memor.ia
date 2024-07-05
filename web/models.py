from django.db import models
from django.conf import settings
from django.urls import reverse

class Planes(models.Model):
    id_plan=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50)
    descripcion=models.TextField()
    cantidad = models.IntegerField()
    valor_factor = models.IntegerField()
    link_pago=models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Planes")
        verbose_name_plural = ("Planess")

    def __str__(self):  
        return self.nombre

    def get_absolute_url(self):
        return reverse("Planes_detail", kwargs={"pk": self.pk})