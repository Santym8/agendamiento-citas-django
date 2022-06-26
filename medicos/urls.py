from django.urls import  path
from . import views
urlpatterns = [
    path('', views.panel_principal, name='panel_medicos'),
    path('registro/', views.registro, name='registro_medicos')
]