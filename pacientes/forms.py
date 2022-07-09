from django import forms
from django.core.exceptions import ValidationError

from phonenumber_field import formfields
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q

from django.contrib.auth.models import User
from .models import Paciente


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password']
        labels = {
            'username': 'Cédula',
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
        
#-------------------------------Fomrulario Paciente---------------------------
class PacienteForm(forms.Form):

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput, 
        required=True, 
        label='Fecha Nacimeinto (yyyy-mm-dd)')
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


#-------------------------------Formulario Actualizar Paciente---------------
class ActualizarPacienteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.id_user = kwargs.pop('id_user',None)
        super(ActualizarPacienteForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        max_length=10, 
        label="Cedula",
        required=True)

    first_name = forms.CharField(
        max_length=30, 
        label="Nombres",
        required=True)

    last_name = forms.CharField(
        max_length=30, 
        label="Apellido",
        required=True)

    email = forms.EmailField(
        label="Email",
        required=True)
    
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput, 
        required=True, 
        label='Fecha Nacimeinto (yyyy-mm-dd)')

    numero_celular = formfields.PhoneNumberField(
        required=True,  
        initial='+593', 
        label='Número celular (Sin 0 inicial)')

    #Verifica que la cedula(username) sea válida
    def clean_username(self):
        user = User.objects.get(id=self.id_user)
        data = self.cleaned_data['username']
        #Solo numeros
        for i in data:
            if i not in ['0','1','2','3','4','5','6','7','8','9']: 
                raise ValidationError('Cédula inválida')
        #10 Caracteres
        if len(data) != 10:
            raise ValidationError('Cédula inválida')
        #Cedula Unica
        user = User.objects.filter(username=data).filter(~Q(id=user.id))
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
        user = User.objects.get(id=self.id_user)
        data = self.cleaned_data['email']
        #No vacia
        if len(data) == 0:
            raise ValidationError('Correo electrónico Vacío')
        #Correo Unico
        user = User.objects.filter(email=data).filter(~Q(id=user.id))
        if user:
            raise ValidationError('Correo electrónico en uso')
        return data

    #Validar Fecha de Nacimiento
    def clean_fecha_nacimiento(self):
        data = self.cleaned_data['fecha_nacimiento']
        edad = relativedelta(datetime.now(), data)
        #Mayor de edad
        if edad.years < 18:
            raise ValidationError('NO puedes crear una cuenta si eres Menor de Edad')
        return data

class CambiarContraseñaForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.id_user = kwargs.pop('id_user',None)
        super(CambiarContraseñaForm, self).__init__(*args, **kwargs)

    contraseña_actual = forms.CharField(required=True, widget=forms.PasswordInput) 
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    verificar_contraseña = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean_contraseña_actual(self):
        data = self.cleaned_data.get('contraseña_actual')
        user = User.objects.get(id = self.id_user)
        if user.password != data:
            raise ValidationError('Contraseña Incorrecta') 
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

