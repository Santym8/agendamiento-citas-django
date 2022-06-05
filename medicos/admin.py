from django.contrib import admin
from .models import Especialidad, Medico
# Register your models here.

class EspecialidadAdmin(admin.ModelAdmin):
    list_display=['id','nombre']


class MedicoAdmin(admin.ModelAdmin):
    list_display = ['id','user','fecha_nacimiento','numero_celular','especialidad','titulo_acreditacion_medica']



admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Medico, MedicoAdmin)