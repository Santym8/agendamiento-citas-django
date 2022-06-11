from django.urls import  path
from . import views
urlpatterns = [
    path('', views.inicio_sesion, name='inicio_medicos'),
    path('registro/', views.registro, name='registro_medicos')
]