from django.urls import  path
from . import views

urlpatterns = [
    path('', views.panel_principal, name='panel_pacientes'),
    path('registro/', views.registro, name='registro_pacientes')
]