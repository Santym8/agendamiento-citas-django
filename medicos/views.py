from django.shortcuts import render
from django.http import HttpResponse
from verify_email.email_handler import send_verification_email
from django.core.files.base import ContentFile
#Modelos
from .models import Medico, Especialidad
from django.contrib.auth.models import User, Group

#Formularios
from .forms import UserForm, MedicoForm



def inicio_sesion(request):
    return HttpResponse("Inicio de sesion")
    
def registro(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        medico_form = MedicoForm(request.POST, request.FILES)
        if user_form.is_valid() and medico_form.is_valid():
            #Guarda usuario
            send_verification_email(request, user_form)
            #Añade usuairo al grupo Medicos
            user = User.objects.get(username=user_form.cleaned_data['username'])
            user.groups.add(Group.objects.get(name='Medicos'))
            #Crea medico con el usuairo creado
            nuevo_medico = Medico(
                user=user, 
                especialidad=medico_form.cleaned_data['especialidad'],
                fecha_nacimiento=medico_form.cleaned_data['fecha_nacimiento'],
                numero_celular=medico_form.cleaned_data['numero_celular'],
                titulo_acreditacion_medica=medico_form.cleaned_data['titulo_acreditacion_medica'])
            nuevo_medico.save()
            return HttpResponse("Medicos funciona")
        else:
            return render(request, 'medicos/registro.html', {'form_usuario': user_form, 'form_medico':medico_form})
    else:
        user_form = UserForm()
        medico_form = MedicoForm()
        return render(request, 'medicos/registro.html', {'form_usuario': user_form, 'form_medico':medico_form})

  
    

    