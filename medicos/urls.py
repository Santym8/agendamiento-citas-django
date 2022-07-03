from django.urls import  path
from . import views
from django.contrib.auth import views as views_django
urlpatterns = [
    path('', views.panel_principal, name='panel_medicos'),
    path('cambiar-estado-turno/<int:id>/<fecha_actual>', views.cambiar_estado_turno, name='estado_turno'),
    path('eliminar-turno/<int:id>/<fecha_actual>', views.eliminar_turno, name='estado_turno'),
    path('registro/', views.registro, name='registro_medicos'),
    path('logout/', views_django.logout_then_login, name='logout-medico')
]