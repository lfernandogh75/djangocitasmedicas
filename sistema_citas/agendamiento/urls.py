# en agendamiento/urls.py
from django.urls import path
from . import views
from .views import paciente_dashboard, cancelar_cita,login_view
 

urlpatterns = [
    # Otras URLs de la aplicación
    path('medico/registrar/', views.registrar_medico, name='registrar_medico'),
    path('medico/dashboard/', views.medico_dashboard, name='medico_dashboard'),
    path('login/medico/', views.login_medico, name='login_medico'),
    path('logout/medico/', views.logout_medico, name='logout_medico'),
    path('paciente/dashboard/', paciente_dashboard, name='paciente_dashboard'),
    path('paciente/cancelar-cita/<int:cita_id>/', cancelar_cita, name='cancelar_cita'),

    path('login/', login_view, name='login_view'),
    path('paciente/dashboard/', paciente_dashboard, name='paciente_dashboard'),
    path('paciente/cancelar-cita/<int:cita_id>/', cancelar_cita, name='cancelar_cita'),
    path('logout/', views.logout_paciente, name='logout'),  
]