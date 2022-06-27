from django.shortcuts import render
from django.http import HttpResponse
from verify_email.email_handler import send_verification_email
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import user_passes_test
from django.template.defaulttags import register
from django.http import HttpResponseRedirect
#Modelos
from .models import Medico, Especialidad, Turno
from django.contrib.auth.models import User, Group
from pacientes.models import Paciente
#Formularios
from .forms import UserForm, MedicoForm, CrearTurno



def registro(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        medico_form = MedicoForm(request.POST, request.FILES)
        if user_form.is_valid() and medico_form.is_valid():
            #Guarda usuario
            #user_form.save()
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

  

def verifica_medico(user):
    return user.groups.filter(name='Medicos').exists()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

@user_passes_test(verifica_medico)
def panel_principal(request):
    medico = Medico.objects.get(user=request.user.id)
    turnos = Turno.objects.filter(medico=medico.id)
    pacientes = {}
    for turno in turnos:
        if turno.paciente is not None:
            paciente = Paciente.objects.get(id=turno.paciente.id)
            user = User.objects.get(id=paciente.user.id)
            pacientes[turno.id] = user.first_name +" "+ user.last_name 
        
    if request.method == 'GET':
        form_crear_turno = CrearTurno(medico=medico)
        return render(request, 'medicos/panel_principal.html', {'turnos':turnos, 'pacientes':pacientes, 'form_crear_turno':form_crear_turno})
    else:
        form_crear_turno = CrearTurno(request.POST,medico=medico)
        if form_crear_turno.is_valid():
            form_crear_turno.save()
            return HttpResponseRedirect('/medicos')
        else:
            return render(request, 'medicos/panel_principal.html', {'turnos':turnos, 'pacientes':pacientes, 'form_crear_turno':form_crear_turno})

    