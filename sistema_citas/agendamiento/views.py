from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medico, Paciente, Cita, Especialidad
from .forms import LoginForm, RegistrarMedicoForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Vista del Dashboard del Médico
@login_required(login_url='login_medico')
def medico_dashboard(request):
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        messages.error(request, "No se encontró el perfil de médico. Contacta al administrador.")
        return render(request, 'agendamiento/error.html', {'message': "No se encontró el perfil de médico."})

    citas = Cita.objects.filter(medico=medico)
    context = {
        'medico': medico,
        'citas': citas
    }
    return render(request, 'agendamiento/medico_dashboard.html', context)

# Vista para Registrar Médico
def registrar_medico(request):
    if request.method == 'POST':
        form = RegistrarMedicoForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'medico'
            user.save()
            Medico.objects.create(usuario=user, especialidad=form.cleaned_data['especialidad'], telefono=form.cleaned_data['telefono'])
            messages.success(request, "Médico registrado con éxito. Ahora puede iniciar sesión.")
            return redirect('login_medico')
    else:
        form = RegistrarMedicoForm()

    return render(request, 'agendamiento/registrar_medico.html', {'form': form})

# Vista para el Login del Médico
def login_medico(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == 'medico':
                login(request, user)
                return redirect('medico_dashboard')
            else:
                messages.error(request, "Credenciales inválidas o no tiene permisos de médico.")
    else:
        form = LoginForm()

    return render(request, 'agendamiento/login_medico.html', {'form': form})

# Vista para cerrar sesión
@login_required
def logout_medico(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('login_medico')

# logica para el paciente  las 3 primeras lineas ya estan al principio
#from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.decorators import login_required
#from .models import Cita, Paciente

@login_required
def paciente_dashboard(request):
    try:
        paciente = request.user.paciente  # Asumiendo que `Paciente` tiene una relación OneToOne con `CustomUser`
        citas = Cita.objects.filter(paciente=paciente)
    except Paciente.DoesNotExist:
        return render(request, 'agendamiento/error.html', {'mensaje': 'No se encontró el perfil de paciente. Contacta al administrador.'})

    return render(request, 'agendamiento/paciente_dashboard.html', {'paciente': paciente, 'citas': citas})

@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, paciente=request.user.paciente)
    
    if cita.estado == 'programada':
        cita.cancelar()
        return redirect('paciente_dashboard')
    else:
        return render(request, 'error.html', {'mensaje': 'No se puede cancelar una cita que ya ha sido completada o cancelada.'})
# fin logica paciente


# logica inicio de sesión las lineas estan en la parte superior 
#from django.contrib.auth import authenticate, login
#from django.shortcuts import render, redirect
#from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Redirigir al dashboard correspondiente según el rol
                if user.role == 'paciente':
                    return redirect('paciente_dashboard')
                elif user.role == 'medico':
                    return redirect('medico_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'agendamiento/login.html', {'form': form})
# fin logica inicio de sesión
@login_required
def logout_paciente(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('login_view')