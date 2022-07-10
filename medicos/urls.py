from django.urls import  path
from . import views
from django.contrib.auth import views as views_django
urlpatterns = [
    #Registro
    path('registro/', views.registro, name='registro_medicos'),
    #Cerra sesion
    path('logout/', views_django.logout_then_login, name='logout-medico'),
    #Panel de creacion Turnos
    path('', views.panel_principal, name='panel_medicos'),
    path('cambiar-estado-turno/<int:id>/<fecha_actual>', views.cambiar_estado_turno, name='estado_turno'),
    path('eliminar-turno/<int:id>/<fecha_actual>', views.eliminar_turno, name='estado_turno'),
    #Actualizar Cuenta
    path('cuenta/', views.actualizar_cuenta, name='cuenta-medico'),
    path('cuenta/datos', views.actualizar_datos, name='cuenta-medico-datos'),
    path('cuenta/contraseña', views.cambiar_contraseña, name='cuenta-medico-cotraseña'),
]