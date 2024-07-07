from django.contrib import admin
from .models import Memorial, Planes, Familiares, Roles, Recuerdos, Usuarios, Usuarios_Planes
# Register your models here.
admin.site.register(Memorial)
admin.site.register(Planes)
admin.site.register(Familiares)
admin.site.register(Roles)
admin.site.register(Recuerdos)
admin.site.register(Usuarios)
admin.site.register(Usuarios_Planes)