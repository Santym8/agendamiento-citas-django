from django.shortcuts import render
from .forms import LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

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
                        return render(request, 'medicos/panel_principal.html')
                    elif user.groups.filter(name='Pacientes').exists():
                        return render(request, 'pacientes/panel_principal.html')
                return render(request, 'login.html', {'login_form':login_form, 'error':'Usuario Desactivado'})
        return render(request, 'login.html', {'login_form':login_form, 'error':'Correo o Contraseña Incorrecta'})
    else:
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form':login_form})