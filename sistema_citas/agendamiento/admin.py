"""
from django.contrib import admin

# Register your models here.
from .models import CustomUser, Especialidad, Medico, Paciente, Cita

admin.site.register(CustomUser)
admin.site.register(Especialidad)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Cita)
"""
"""
from django.contrib import admin
from .models import CustomUser, Especialidad, Medico, Paciente, Cita
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Clase Inline para Citas
class CitaInline(admin.TabularInline):  # También puedes usar admin.StackedInline
    model = Cita
    extra = 1
    fields = ['paciente', 'fecha_hora', 'motivo', 'estado']
    readonly_fields = ['estado']
    fk_name = 'medico'

# Configuración del Administrador para CustomUser
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Configuración del Administrador para Especialidad
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

# Configuración del Administrador para Medico con Inlines
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'especialidad', 'telefono']
    search_fields = ['usuario__username', 'especialidad__nombre']
    list_filter = ['especialidad']
    inlines = [CitaInline]  # Agregar la clase Inline

# Configuración del Administrador para Paciente
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefono', 'direccion']
    search_fields = ['usuario__username', 'direccion']

# Configuración del Administrador para Cita
class CitaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'medico', 'fecha_hora', 'estado']
    search_fields = ['paciente__usuario__username', 'medico__usuario__username']
    list_filter = ['estado', 'fecha_hora']
    date_hierarchy = 'fecha_hora'


# Registro de modelos en el administrador
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Cita, CitaAdmin) 
 
 """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Medico, Paciente, Cita, Especialidad
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Especialidad)

