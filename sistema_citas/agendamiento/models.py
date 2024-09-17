from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo de Usuario Personalizado
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='paciente')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Modelo de Especialidad
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

# Modelo de Médico
class Medico(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'medico'})
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.especialidad.nombre}"

# Modelo de Paciente
class Paciente(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'paciente'})
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()}"

# Modelo de Cita
class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas_paciente')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=[
        ('programada', 'Programada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], default='programada')

    def __str__(self):
        return f"Cita: {self.paciente.usuario.get_full_name()} con {self.medico.usuario.get_full_name()} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"

    def cancelar(self):
        if self.estado != 'completada':
            self.estado = 'cancelada'
            self.save()
        else:
            raise ValueError("No se puede cancelar una cita completada.")
