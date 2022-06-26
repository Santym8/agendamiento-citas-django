from django.shortcuts import render
from .forms import LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect

def inicio_sesion(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if(login_form.is_valid()):
            try:
                user = User.objects.get(email=login_form.cleaned_data['correo'])
            except User.DoesNotExist:
                user = None
            if(user is not None and user.password == login_form.cleaned_data['contraseña']):
                if(user.is_active):
                    login(request, user)
                    if user.groups.filter(name='Medicos').exists():
                        return HttpResponseRedirect('medicos/')
                    elif user.groups.filter(name='Pacientes').exists():
                        return HttpResponseRedirect('pacientes/')
                return render(request, 'Login2.html', {'login_form':login_form, 'error':'Usuario Desactivado'})
        return render(request, 'Login2.html', {'login_form':login_form, 'error':'Correo o Contraseña Incorrecta'})
    else:
        login_form = LoginForm()
        return render(request, 'Login2.html', {'login_form':login_form})