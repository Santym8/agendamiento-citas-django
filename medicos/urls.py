from django.urls import  path
from . import views
urlpatterns = [
    path('', views.panel_principal, name='panel_medicos'),
    path('cambiar-estado-turno/<int:id>', views.cambiar_estado_turno, name='estado_turno'),
    path('eliminar-turno/<int:id>', views.eliminar_turno, name='estado_turno'),
    path('registro/', views.registro, name='registro_medicos')
]