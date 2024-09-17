from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Medico

@receiver(post_save, sender=CustomUser)
def crear_perfil_medico(sender, instance, created, **kwargs):
    if created and instance.role == 'medico':
        # Verificar si ya existe un perfil de Medico para evitar duplicados
        if not hasattr(instance, 'medico'):
            Medico.objects.create(usuario=instance)
