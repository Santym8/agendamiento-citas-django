from django.shortcuts import render
from django.http import HttpResponse
from verify_email.email_handler import send_verification_email
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
#Modelos
from .models import Paciente
from django.contrib.auth.models import User, Group
from medicos.models import Turno, Medico, Especialidad
#Formularios
from .forms import UserForm, PacienteForm
#Python
from datetime import datetime, timedelta, date
    
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
            return render(request,'validacion_email/email.html',{'email':user_form['email']})
            # return HttpResponse("Pacientes funciona")
        else:
            return render(request, 'pacientes/registro.html', {'user_form': user_form, 'paciente_form':paciente_form})
    else:
        user_form = UserForm()
        paciente_form = PacienteForm()
        return render(request, 'pacientes/registro.html', {'user_form': user_form, 'paciente_form':paciente_form})



#----------------------------------------------Panel Principal--------------------------------

def verifica_paciente(user):
    return user.groups.filter(name='Pacientes').exists()


def get_turnos_semana(fecha, id_especialidad):
    inicio_semana = fecha - timedelta(days=fecha.weekday())
    fin_semana = inicio_semana + timedelta(days=7)

    #Busca todos los turnos en las fechas establecidas y de la especialidad definida, EL truno debe estar libre y no completado
    turnos = Turno.objects.filter(fecha__gte=inicio_semana, fecha__lt=fin_semana,paciente=None, completado=False, medico__especialidad=id_especialidad).order_by('fecha')

    fechas_agrupadas = {}
    for i in range(7):
        fecha_grupo = inicio_semana+timedelta(days=i)
        fechas_agrupadas[fecha_grupo] = turnos.filter(fecha__gte=fecha_grupo, fecha__lt=fecha_grupo+timedelta(days=1))

    return fechas_agrupadas

@user_passes_test(verifica_paciente)
def panel_principal(request, especialidad=None):


    #Mensaje a deplegarse
    mensaje = request.GET.get('mensaje')

    if(especialidad is None):
        #Escoje la primiera especialidad encontrada
            especialidad = Especialidad.objects.all()[0]
    else:
        #Verifica que la especialidad exista
        try:
            especialidad = Especialidad.objects.get(nombre=especialidad)
        except Especialidad.DoesNotExist:
            especialidad = Especialidad.objects.all()[0]


    #Recibe la fecha a mostrarse
    fecha = request.GET.get('fecha')
    if(fecha is None):
        fecha = date.today()
    else:
        fecha = datetime.strptime(fecha, '%d-%m-%Y')
    #Recibe el id de la especialidad a mostrarse
   

    turnos = get_turnos_semana(fecha, especialidad.id)

    #Guarda el nombre completo de cada Medico de un turno
    medicos = {}
    direcciones_medicos = {}
    for turnos_dia in turnos:
        turnos_dia = turnos[turnos_dia]
        for turno in turnos_dia:
            medico = Medico.objects.get(id=turno.medico.id)
            user = User.objects.get(id=medico.user.id)
            medicos[turno.id] = user.first_name +" "+ user.last_name 
            direcciones_medicos[turno.id] = medico.direccion
            

    #Calcula las fechas sugiente y anteriror
    anterior_semana = (fecha - timedelta(days=fecha.weekday())) - timedelta(days=7)
    siguiente_semana = (fecha - timedelta(days=fecha.weekday())) + timedelta(days=7)

    return render(request, 'pacientes/panel_principal.html', 
        {'turnos':turnos, 
        'medicos':medicos, 
        'direcciones_medicos':direcciones_medicos,
        'siguiente_semana':siguiente_semana,
        'anterior_semana':anterior_semana,
        'especialidad_mostrada':especialidad.nombre,
        'fecha_mostrada': fecha,
        'especialidades':Especialidad.objects.all(),
        'mensaje':mensaje
        })


    return render(request, 'pacientes/panel_principal.html')

@user_passes_test(verifica_paciente)
def agendar_cita(request, id_turno, fecha_mostrada, especialidad_mostrada):
    try:
        turno = Turno.objects.get(id=id_turno, completado=False, paciente=None)
        paciente = Paciente.objects.get(user=request.user.id)
        #Comprueba conflicto de horarios del paciente
        if(Turno.objects.filter(fecha=turno.fecha, paciente=paciente.id).exists()):
            return HttpResponseRedirect('/pacientes/'+ especialidad_mostrada+ '?fecha='+fecha_mostrada+'&mensaje=Conflicto de Horarios')
        turno.paciente = paciente
        turno.save()
        return HttpResponseRedirect('/pacientes/'+ especialidad_mostrada+ '?fecha='+fecha_mostrada+'&mensaje=Cita Agendada')
    except Turno.DoesNotExist:
        return HttpResponseRedirect('/pacientes/'+ especialidad_mostrada+ '?fecha='+fecha_mostrada+'&mensaje=Error: El turno se ha ocupado')

    
