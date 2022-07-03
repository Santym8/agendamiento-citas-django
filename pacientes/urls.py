from django.urls import  path
from . import views
from django.contrib.auth import views as views_django
urlpatterns = [
    path('', views.panel_principal, name='panel_pacientes'),
    path('<especialidad>', views.panel_principal, name='panel_pacientes'),
    path('registro/', views.registro, name='registro_pacientes'),
    path('agendar_cita/<id_turno>/<fecha_mostrada>/<especialidad_mostrada>', views.agendar_cita, name='agendar-cita'),
     path('logout/', views_django.logout_then_login, name='logout-paciente')
]