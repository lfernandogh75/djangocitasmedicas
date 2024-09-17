from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser, Especialidad

# Formulario de Login
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

# Formulario para Registrar Médicos
class RegistrarMedicoForm(UserCreationForm):
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all(), label='Especialidad')
    telefono = forms.CharField(label='Teléfono', max_length=20)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'especialidad', 'telefono']
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
        }

# CustomUserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']
# CustomUserChangeForm
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']


