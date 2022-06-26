from django.shortcuts import render
from django.http import HttpResponse
from verify_email.email_handler import send_verification_email
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import user_passes_test
#Modelos
from .models import Paciente
from django.contrib.auth.models import User, Group

#Formularios
from .forms import UserForm, PacienteForm
    
def registro(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        paciente_form = PacienteForm(request.POST, request.FILES)
        if user_form.is_valid() and paciente_form.is_valid():
            #Guarda usuario
            #user_form.save()
            send_verification_email(request, user_form)
            #Añade usuairo al grupo Pacientes
            user = User.objects.get(username=user_form.cleaned_data['username']) 
            user.groups.add(Group.objects.get(name='Pacientes'))
            #Crea Paciente con el usuairo creado
            nuevo_paciente = Paciente(
                user=user, 
                fecha_nacimiento=paciente_form.cleaned_data['fecha_nacimiento'],
                numero_celular=paciente_form.cleaned_data['numero_celular'])
            nuevo_paciente.save()
            return HttpResponse("Pacientes funciona")
        else:
            return render(request, 'pacientes/registro.html', {'user_form': user_form, 'paciente_form':paciente_form})
    else:
        user_form = UserForm()
        paciente_form = PacienteForm()
        return render(request, 'pacientes/registro.html', {'user_form': user_form, 'paciente_form':paciente_form})

def verifica_paciente(user):
    return user.groups.filter(name='Pacientes').exists()

def panel_principal(request):
    return render(request, 'pacientes/panel_principal.html')
