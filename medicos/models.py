from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Especialidad(models.Model):
    nombre = models.CharField('Nombre',max_length=30)

    def __str__(self):
        return self.nombre

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField('Fecha nacimiento')
    numero_celular = PhoneNumberField('Numero Celular')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    titulo_acreditacion_medica = models.FileField('Titulo',upload_to='archivos/titulos')
    verificado = models.BooleanField(default=False)