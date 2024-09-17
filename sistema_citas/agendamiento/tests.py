from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Especialidad, Medico, Paciente, Cita

CustomUser = get_user_model()

class CustomUserTest(TestCase):
    def setUp(self):
        # Crear usuarios de prueba
        self.admin_user = CustomUser.objects.create_user(
            username='admin', email='admin@example.com', password='adminpass', role='admin')
        self.medico_user = CustomUser.objects.create_user(
            username='doctor', email='doctor@example.com', password='medicopass', role='medico')
        self.paciente_user = CustomUser.objects.create_user(
            username='paciente', email='paciente@example.com', password='pacientepass', role='paciente')

        # Crear especialidades
        self.cardiologia = Especialidad.objects.create(nombre='Cardiología', descripcion='Especialidad en enfermedades del corazón')
        self.neurologia = Especialidad.objects.create(nombre='Neurología', descripcion='Especialidad en el sistema nervioso')

        # Asignar especialidades a los médicos
        self.medico = Medico.objects.create(usuario=self.medico_user, especialidad=self.cardiologia, telefono='123456789')

        # Crear pacientes
        self.paciente = Paciente.objects.create(usuario=self.paciente_user, telefono='987654321', direccion='123 Calle Falsa')

        # Crear una cita
        self.cita = Cita.objects.create(paciente=self.paciente, medico=self.medico, fecha_hora=timezone.now(), motivo='Consulta general', estado='programada')

    def test_admin_user_creation(self):
        # Verificar que el usuario administrador tenga el rol correcto
        self.assertEqual(self.admin_user.role, 'admin')
        self.assertTrue(self.admin_user.is_active)

    def test_medico_user_creation(self):
        # Verificar que el usuario médico tenga el rol correcto
        self.assertEqual(self.medico_user.role, 'medico')
        self.assertTrue(self.medico_user.is_active)
        self.assertEqual(self.medico.especialidad, self.cardiologia)

    def test_paciente_user_creation(self):
        # Verificar que el usuario paciente tenga el rol correcto
        self.assertEqual(self.paciente_user.role, 'paciente')
        self.assertTrue(self.paciente_user.is_active)
        self.assertEqual(self.paciente.telefono, '987654321')

    def test_cita_creation(self):
        # Verificar que la cita se haya creado correctamente
        self.assertEqual(self.cita.paciente, self.paciente)
        self.assertEqual(self.cita.medico, self.medico)
        self.assertEqual(self.cita.motivo, 'Consulta general')
        self.assertEqual(self.cita.estado, 'programada')

    def test_medico_especialidad_change(self):
        # Cambiar la especialidad del médico y verificar
        self.medico.especialidad = self.neurologia
        self.medico.save()
        self.assertEqual(self.medico.especialidad, self.neurologia)

  
