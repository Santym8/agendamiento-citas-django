from django.shortcuts import render
from django.http import HttpResponse
#Modelos
from .models import Medico, Especialidad
from django.contrib.auth.models import User, Group

#Formularios
from .forms import UserForm, MedicoForm
def inicio(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        medico_form = MedicoForm(request.POST)
        if user_form.is_valid() and medico_form.is_valid():
            #Guarda usuario
            user_form.save()
            #Añade usuairo al grupo Medicos
            user = User.objects.get(username=user_form.cleaned_data['username'])
            user.groups.add(Group.objects.get(name='Medicos'))
            #Crea medico con el usuairo creado
            nuevo_medico = Medico(
                user=user, 
                especialidad=medico_form.cleaned_data['especialidad'],
                fecha_nacimiento=medico_form.cleaned_data['fecha_nacimiento'],
                numero_celular=medico_form.cleaned_data['numero_celular'])
            nuevo_medico.save()
            return HttpResponse("Medicos funciona")
        else:
            return render(request, 'medicos/inicio.html', {'form_usuario': user_form, 'form_medico':medico_form})
    else:
        user_form = UserForm()
        medico_form = MedicoForm()
        return render(request, 'medicos/inicio.html', {'form_usuario': user_form, 'form_medico':medico_form})

  
    

    