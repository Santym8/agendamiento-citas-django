from django.urls import  path
from . import views
from django.contrib.auth import views as views_django
urlpatterns = [
    #Registro
    path('registro/', views.registro, name='registro_pacientes'),
    #Cerrar Sesion
    path('logout/', views_django.logout_then_login, name='logout-paciente'),
    #Panel De Agendameinto
    path('', views.panel_principal, name='panel_pacientes'),
    path('<especialidad>', views.panel_principal, name='panel_pacientes'),
    path('agendar_cita/<id_turno>/<fecha_mostrada>/<especialidad_mostrada>', views.agendar_cita, name='agendar-cita'),
    #Panel Mis Citas
    path('mis_citas/', views.mis_citas, name='mis_citas'),
    path('mis_citas/<especialidad>', views.mis_citas, name='mis_citas'),
    path('mis_citas/cancelar_cita/<id_turno>/<fecha_mostrada>/<especialidad_mostrada>', views.cancelar_cita, name='agendar-cita'),
    #Actualizar Cuenta
    path('cuenta/', views.actualizar_cuenta, name='cuenta'),
    path('cuenta/datos', views.actualizar_datos, name='cuenta-datos'),
    path('cuenta/contraseña', views.cambiar_contraseña, name='cuenta-cotraseña'),
]