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
#Python
from datetime import datetime, timedelta, date



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
            return render(request,'validacion_email/email.html',{'email':user_form['email']})
            #return HttpResponse("Medicos funciona")
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



def get_turnos_semana(fecha, id):
    inicio_semana = fecha - timedelta(days=fecha.weekday())
    fin_semana = inicio_semana + timedelta(days=7)
    turnos = Turno.objects.filter(fecha__gte=inicio_semana, fecha__lt=fin_semana, medico=id).order_by('fecha')

    fechas_agrupadas = {}

    for i in range(7):
        fecha_grupo = inicio_semana+timedelta(days=i)
        fechas_agrupadas[fecha_grupo] = turnos.filter(fecha__gte=fecha_grupo, fecha__lt=fecha_grupo+timedelta(days=1))

    return fechas_agrupadas

@user_passes_test(verifica_medico)
def panel_principal(request):
    #Obiene la fecha de la semana que debe mostrar
    fecha = request.GET.get('fecha')
    if(fecha is None):
        fecha = date.today()
    else:
        fecha = datetime.strptime(fecha, '%d-%m-%Y')
    #Obtiene datos del medico
    medico = Medico.objects.get(user=request.user.id)
    #Obtiene los turno
    turnos = get_turnos_semana(fecha, medico.id)

    #Guarda el nombre completo de cada paciente que a agendado una cita
    pacientes = {}
    for turnos_dia in turnos:
        turnos_dia = turnos[turnos_dia]
        for turno in turnos_dia:
            if turno.paciente is not None:
                paciente = Paciente.objects.get(id=turno.paciente.id)
                user = User.objects.get(id=paciente.user.id)
                pacientes[turno.id] = user.first_name +" "+ user.last_name 

    #Calcula las fechas sugiente y anteriror
    anterior_semana = (fecha - timedelta(days=fecha.weekday())) - timedelta(days=7)
    siguiente_semana = (fecha - timedelta(days=fecha.weekday())) + timedelta(days=7)


    if request.method == 'GET':
        form_crear_turno = CrearTurno(medico=medico)
        return render(request, 'medicos/panel_principal.html', 
            {'turnos':turnos, 
            'pacientes':pacientes, 
            'form_crear_turno':form_crear_turno, 
            'siguiente_semana':siguiente_semana,
            'anterior_semana':anterior_semana,
            'fecha_mostrada': fecha
            })
    else:
        form_crear_turno = CrearTurno(request.POST,medico=medico)
        if form_crear_turno.is_valid():
            form_crear_turno.save()
            #Sirve para llevar al usuario a ver la semana en la cual se inserto la fecha
            fecha_guardada = form_crear_turno.cleaned_data['fecha']
            fecha_guardada = str(fecha_guardada.day) + "-" + str(fecha_guardada.month) + "-" + str(fecha_guardada.year)
            return HttpResponseRedirect('/medicos?fecha='+fecha_guardada)
        else:
            return render(request, 'medicos/panel_principal.html', 
                {'turnos':turnos, 
                'pacientes':pacientes, 
                'form_crear_turno':form_crear_turno, 
                'siguiente_semana':siguiente_semana,
                'anterior_semana':anterior_semana,
                'fecha_mostrada': fecha
                })

@user_passes_test(verifica_medico)
def cambiar_estado_turno(request, id, fecha_actual):
    medico = Medico.objects.get(user=request.user.id)
    try:
        turno = Turno.objects.get(medico=medico.id, id=id)
    except turno.DoesNotExist:
        turno = None
    if(turno):
        turno.completado = not turno.completado 
        turno.save()    

    return HttpResponseRedirect('/medicos?fecha='+fecha_actual)


@user_passes_test(verifica_medico)
def eliminar_turno(request, id, fecha_actual):
    medico = Medico.objects.get(user=request.user.id)
    try:
        turno = Turno.objects.get(medico=medico.id, id=id)
    except turno.DoesNotExist:
        turno = None
    if(turno):
        if(turno.paciente):
            #To-do enviar correo al paciente
            pass
        turno.delete()  
    return HttpResponseRedirect('/medicos?fecha='+fecha_actual)