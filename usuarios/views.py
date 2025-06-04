from django.shortcuts import render, redirect
from .forms import RegistroForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from conferencia.models import Conferencia
from conferencia.models import InvitacionRevisor
from django.shortcuts import get_object_or_404
from notificaciones.models import Notificacion


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    success_message = "Se han enviado las instrucciones para restablecer tu contraseña a tu correo electrónico."

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'  # Personaliza este template
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)

                # Redirigir según el grupo al que pertenece
                if user.groups.filter(name='Autor').exists():
                    return redirect('vistaAutor')
                elif user.groups.filter(name='Organizador').exists():
                    return redirect('vistaOrganizador')
                elif user.groups.filter(name='Revisor').exists():
                    return redirect('vistaRevisor')
                elif user.groups.filter(name='Administrador').exists():  # <- Aquí va "Administrador"
                    return redirect('vistaAdmin')
                else:
                    messages.error(request, "No tienes un rol asignado.")
                    return redirect('login')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # A donde quieras redirigir después de cerrar sesión

# Vistas para cada grupo
@login_required
def vistaAutor(request):
    is_revisor = request.user.groups.filter(name='Revisor').exists()
    is_organizador = request.user.groups.filter(name='Organizador').exists()
    is_administrador = request.user.groups.filter(name='Administrador').exists()
    return render(request, 'usuarios/vistaAutor.html', {
        'is_organizador': is_organizador,
        'is_revisor': is_revisor,
        'is_administrador': is_administrador,})

@login_required
def vistaOrganizador(request):
    is_revisor = request.user.groups.filter(name='Revisor').exists()
    is_organizador = request.user.groups.filter(name='Organizador').exists()
    is_administrador = request.user.groups.filter(name='Administrador').exists()
    return render(request, 'usuarios/vistaOrganizador.html', {
        'is_organizador': is_organizador,
        'is_revisor': is_revisor,
        'is_administrador': is_administrador,})


@login_required
def vistaRevisor(request):
    is_revisor = request.user.groups.filter(name='Revisor').exists()
    is_organizador = request.user.groups.filter(name='Organizador').exists()
    is_administrador = request.user.groups.filter(name='Administrador').exists()
    return render(request, 'usuarios/vistaRevisor.html', {
        'is_organizador': is_organizador,
        'is_revisor': is_revisor,
        'is_administrador': is_administrador,})

@login_required
def vistaAdmin(request):
    is_revisor = request.user.groups.filter(name='Revisor').exists()
    is_organizador = request.user.groups.filter(name='Organizador').exists()
    is_administrador = request.user.groups.filter(name='Administrador').exists()
    return render(request, 'usuarios/vistaAdmin.html', {
        'is_organizador': is_organizador,
        'is_revisor': is_revisor,
        'is_administrador': is_administrador,})


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Obtener el correo y usarlo como username
            email = form.cleaned_data['email']
            username = email  # Usamos el correo como username
            
            # Comprobamos si ya existe un usuario con el mismo correo
            if CustomUser.objects.filter(email=email).exists():
                form.add_error('email', 'Este correo ya está registrado.')
                return render(request, 'usuarios/registro.html', {'form': form})

            # Crear el usuario
            user = form.save(commit=False)
            user.username = username  # Asignamos el correo como username
            user.set_password(form.cleaned_data['password1'])  # Aseguramos de establecer la contraseña correctamente
            
            # Asignamos los campos nombre y apellidos del formulario al usuario
            user.nombre = form.cleaned_data['nombre']
            user.apellidos = form.cleaned_data['apellidos']
            
            user.save()

            # Asignar el rol de Autor (o el que corresponda)
            autor_group, _ = Group.objects.get_or_create(name='Autor') 
            user.groups.add(autor_group)

            # Iniciar sesión automáticamente
            login(request, user)
            messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
            return redirect('login')  # Redirigir a la vista de autor
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def admin_dashboard(request):
    # Obtener todos los usuarios del sistema
    users = CustomUser.objects.all()

    # Pasar los usuarios a la plantilla
    return render(request, 'usuarios/admin_dashboard.html', {'users': users})

@login_required
def actualizar_roles(request):
    if request.method == 'POST':
        users = CustomUser.objects.all()
        for user in users:
            # Evaluamos por cada rol
            for rol in ['Organizador', 'Revisor', 'Administrador']:
                checkbox_name = f'roles_{user.id}_{rol.lower()}'
                grupo, _ = Group.objects.get_or_create(name=rol)

                if checkbox_name in request.POST:
                    user.groups.add(grupo)
                else:
                    user.groups.remove(grupo)
        return redirect('admin_dashboard')  # o la vista que uses para mostrar los usuarios
    
@login_required
def actualizar_roles(request):
    if request.method == 'POST':
        users = CustomUser.objects.all()
        for user in users:
            for rol in ['Organizador', 'Revisor', 'Administrador']:
                checkbox_name = f'roles_{user.id}_{rol.lower()}'
                grupo, _ = Group.objects.get_or_create(name=rol)

                tiene_rol = grupo in user.groups.all()
                check_enviado = checkbox_name in request.POST

                if check_enviado and not tiene_rol:
                    # Se le asignó un nuevo rol
                    user.groups.add(grupo)
                    Notificacion.objects.create(
                        usuario=user,
                        mensaje=f"Se te ha asignado el rol de {rol}."
                    )
                elif not check_enviado and tiene_rol:
                    # Se le removió un rol
                    user.groups.remove(grupo)
                    Notificacion.objects.create(
                        usuario=user,
                        mensaje=f"Se te ha removido el rol de {rol}."
                    )

        return redirect('admin_dashboard')

    
@login_required
def admin_dashboard_view(request):
    usuarios = CustomUser.objects.all().prefetch_related('groups')
    
    # Agregamos la lista de roles al usuario para facilitar el uso en el template
    for user in usuarios:
        user.roles = list(user.groups.values_list('name', flat=True))
    
    return render(request, 'administrador/admin_dashboard.html', {
        'usuarios': usuarios
    })

@login_required
def vista_organizador(request):
    conferencias = Conferencia.objects.filter(organizador=request.user)
    return render(request, 'usuarios/vistaOrganizador.html', {'conferencias': conferencias})

@login_required
def invitaciones_autor_view(request):
    usuario = request.user
    invitaciones = InvitacionRevisor.objects.filter(autor=usuario)

    return render(request, 'usuarios/invitaciones.html', {'invitaciones': invitaciones})

@login_required
def responder_invitacion_revisor_view(request, invitacion_id):
    invitacion = get_object_or_404(InvitacionRevisor, id=invitacion_id, autor=request.user)

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        if respuesta == 'aceptar':
            invitacion.estado = 'aceptado'
            
            # Asignar al grupo "Revisor" si no está ya
            grupo_revisor, _ = Group.objects.get_or_create(name='Revisor')
            if not request.user.groups.filter(name='Revisor').exists():
                request.user.groups.add(grupo_revisor)

        elif respuesta == 'rechazar':
            invitacion.estado = 'rechazado'

        invitacion.save()

    return redirect('invitaciones_autor')
