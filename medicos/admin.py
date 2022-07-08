from django.contrib import admin
from django.utils.html import format_html
from .models import Especialidad, Medico, Turno
# Register your models here.

class EspecialidadAdmin(admin.ModelAdmin):
    list_display=['id','nombre']


class MedicoAdmin(admin.ModelAdmin):
    list_display = ['id','user','fecha_nacimiento','numero_celular','especialidad','direccion','titulo_acreditacion_medica', 'verificado', 'pdf']
    list_filter = ['verificado']
    def pdf(self, obj):
        return format_html('<a href="{}"> Ver </a>', obj.titulo_acreditacion_medica.url)

class TurnoAdmin(admin.ModelAdmin):
    list_display = ['id', 'medico', 'paciente', 'fecha', 'completado']


admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Turno, TurnoAdmin)