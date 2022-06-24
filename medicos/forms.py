from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from phonenumber_field import formfields
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from .models import Medico


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password']
        labels = {
            'username': 'Cédula',
        }
        widgets = {
            'username':forms.TextInput(attrs={"placeholder":"1002003004"}),
            'last_name': forms.TextInput(attrs={"placeholder":"Flores"}),
            'first_name':forms.TextInput(attrs={"placeholder":"Leonardo"}),
            'email':forms.TextInput(attrs={"placeholder":"leonardoflores@correo.com"})
        }
        
    verificar_contraseña = forms.CharField(required=True)
    #Verifica que la cedula(username) sea válida
    def clean_username(self):
        data = self.cleaned_data['username']
        #Solo numeros
        for i in data:
            if i not in ['0','1','2','3','4','5','6','7','8','9']: 
                raise ValidationError('Cédula inválida')
        #10 Caracteres
        if len(data) != 10:
            raise ValidationError('Cédula inválida')
        #Cedula Unica
        user = User.objects.filter(username=data)
        if user:
            raise ValidationError('Ya existe un Usuario con este Número de Cédula')
        return data

    
    #Verifica Nombre solo letras
    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        #No este vacia
        if len(data) == 0:
            raise ValidationError('Nombre Vacío')
        #No contiene Numeros
        for i in data:
            if i in ['0','1','2','3','4','5','6','7','8','9']: 
                raise ValidationError('Nombre no debe contener Números')
        return data

    #Verifica Apellido solo letras
    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        #No vacia
        if len(data) == 0:
            raise ValidationError('Apellido Vacío')
        #No tenga Numeros
        for i in data:
            if i in ['0','1','2','3','4','5','6','7','8','9']: 
                raise ValidationError('Apellido no debe contener Números')
        return data

    #Verifica que el email es unico
    def clean_email(self):
        data = self.cleaned_data['email']
        #No vacia
        if len(data) == 0:
            raise ValidationError('Correo electrónico Vacío')
        #Correo Unico
        user = User.objects.filter(email=data)
        if user:
            raise ValidationError('Correo electrónico en uso')
        return data

    #Verifica confirmacion contraseña
    def clean_verificar_contraseña(self):
        contraseña = self.cleaned_data.get('password')
        verificar_contraseña = self.cleaned_data['verificar_contraseña']
        if len(contraseña) < 8:
            raise ValidationError('La contraseña debe tener mas de 8 caracteres') 
        if contraseña != verificar_contraseña:
            raise ValidationError('No coinciden contraseñas')
        return verificar_contraseña
        
#-------------------------------Fomrulario Medicos---------------------------
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especialidad', 'titulo_acreditacion_medica']

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder":"(yyyy-mm-dd)"}), 
        required=True, 
        label='Fecha Nacimeinto')
    numero_celular = formfields.PhoneNumberField(
        required=True,  
        initial='+593', 
        label='Número celular (Sin 0 inicial)')
    
    #Validar Fecha de Nacimiento
    def clean_fecha_nacimiento(self):
        data = self.cleaned_data['fecha_nacimiento']
        edad = relativedelta(datetime.now(), data)
        #Mayor de edad
        if edad.years < 18:
            raise ValidationError('NO puedes crear una cuenta si eres Menor de Edad')
        return data
