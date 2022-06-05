from django import forms
from django.core.exceptions import ValidationError

from phonenumber_field import formfields
from phonenumber_field.widgets import PhonePrefixSelect

from django.contrib.auth.models import User
from .models import Medico


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

    #Verifica que la cedula sea válida
    def clean_username(self):
        data = self.cleaned_data['username']
        for i in data:
            if i not in ['0','1','2','3','4','5','6','7','8','9',]: 
                raise ValidationError('Cédula inválida')
        if len(data) != 10:
            raise ValidationError('Cédula inválida')
        return data

    #Verifica que el email es unico
    def clean_email(self):
        data = self.cleaned_data['email']
        user = User.objects.filter(email=data)
        if user:
            raise ValidationError('Correo electrónico en uso')
        return data


#-------------------------------Fomrulario Medicos---------------------------
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especialidad']

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput, 
        required=True, 
        label='Fecha Nacimeinto (yyyy-mm-dd)')
    numero_celular = formfields.PhoneNumberField(
        required=True,  
        initial='+593', 
        label='Número celular (Si 0 inicial)')

