from django.contrib import admin
from .models import Paciente
# Register your models here.


class PacienteAdmin(admin.ModelAdmin):
    list_display = ['id','user','fecha_nacimiento','numero_celular']

admin.site.register(Paciente, PacienteAdmin)