from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse_lazy

from .forms import *

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import View

from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from flask import Flask, redirect, url_for, session



# Vistas de Franco Lopez Hiriart

#___________________Generales

def home (request):
    return render (request, "aplication/index.html")

def acerca(request):
    return render(request, "aplication/acerca_de_mi.html") 


#___________________Equipo

@login_required
def equipos (request):
    contexto = {Equipo.objects.all()}
    return render (request, "aplication/equipo_list.html", contexto)

class EquipoList(ListView,LoginRequiredMixin):
    model = Equipo

class EquipoCreate(CreateView,LoginRequiredMixin):
    model = Equipo
    fields = ["nombre", "abreviatura", "ciudad"]
    success_url = reverse_lazy("equipos")

class EquipoUpdate(UpdateView,LoginRequiredMixin):
    model = Equipo
    fields = ["nombre", "abreviatura", "ciudad"]
    success_url = reverse_lazy("equipos")

class EquipoDelete(DeleteView,LoginRequiredMixin):
    model = Equipo
    success_url = reverse_lazy("equipos")  

@login_required
def buscarEquipos(request):
    return render (request, "aplication/equipo_buscar.html")

@login_required
def encontrarEquipos(request):
    if 'buscar' in request.GET:
        patron = request.GET["buscar"]
        equipos = Equipo.objects.filter(nombre__icontains=patron)
        contexto = {"equipos": equipos}
        return render(request, "aplication/equipo_list.html", contexto)
    
    contexto = {"equipos": Equipo.objects.all()}
    return render(request, "aplication/equipo_list.html", contexto) 

#___________________Jugadores
    
@login_required
def jugadores (request):
    contexto = {Jugador.objects.all()}
    return render (request, "aplication/jugador_list.html", contexto)

class JugadorList(ListView,LoginRequiredMixin):
    model = Jugador

class JugadorCreate(CreateView,LoginRequiredMixin):
    model = Jugador
    fields = ["nombre", "apellido", "equipo", "edad"]
    success_url = reverse_lazy("jugadores")

class JugadorUpdate(UpdateView,LoginRequiredMixin):
    model = Jugador
    fields = ["nombre", "apellido", "equipo", "edad"]
    success_url = reverse_lazy("jugadores")

class JugadorDelete(DeleteView,LoginRequiredMixin):
    model = Jugador
    success_url = reverse_lazy("jugadores")  


#___________________DirectoresTecnicos
    
@login_required
def directores_tecnicos (request):
    contexto = {DirectorTecnico.objects.all()}
    return render (request, "aplication/directortecnico_list.html", contexto)

class DirectorTecnicoList(ListView,LoginRequiredMixin):
    model = DirectorTecnico

class DirectorTecnicoCreate(CreateView,LoginRequiredMixin):
    model = DirectorTecnico
    fields = ["nombre", "apellido", "email", "equipo"]
    success_url = reverse_lazy("directores_tecnicos")

class DirectorTecnicoUpdate(UpdateView,LoginRequiredMixin):
    model = DirectorTecnico
    fields = ["nombre", "apellido","email", "equipo"]
    success_url = reverse_lazy("directores_tecnicos")

class DirectorTecnicoDelete(DeleteView,LoginRequiredMixin):
    model = DirectorTecnico
    success_url = reverse_lazy("directores_tecnicos") 

#___________________DirectoresTecnicos
    
@login_required
def nuevos_talentos (request):
    contexto = {Talento.objects.all()}
    return render (request, "aplication/talento_list.html", contexto)

class TalentoList(ListView,LoginRequiredMixin):
    model = Talento

class TalentoCreate(CreateView,LoginRequiredMixin):
    model = Talento
    fields = ["nombre", "apellido", "equipo", "edad"]
    success_url = reverse_lazy("talentos")

class TalentoUpdate(UpdateView,LoginRequiredMixin):
    model = Talento
    fields = ["nombre", "apellido", "equipo", "edad"]
    success_url = reverse_lazy("talentos")

class TalentoDelete(DeleteView,LoginRequiredMixin):
    model = Talento
    success_url = reverse_lazy("talentos") 

#___________________Registro y Autenticacion
    
def login_request(request):         
    if request.method == "POST":
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)

            #______ Avatar
            
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar

            #________________________________________________________

            return render(request, "aplication/index.html")
        else:
            return redirect(reverse_lazy('login'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = AuthenticationForm()

    return render(request, "aplication/login.html", {"form": miForm} )

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('logout')

def register(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)

        if miForm.is_valid():
            usuario = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('index'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = RegistroForm()

    return render(request, "aplication/registro.html", {"form": miForm} )  

#________________________ Edición de Perfil, Cambio Clave, Avatar

@login_required
def editProfile(request):
    usuario = request.user
    if request.method == "POST":
        miForm = UserEditForm(request.POST)
        if miForm.is_valid():
            user = User.objects.get(username=usuario)
            user.email = miForm.cleaned_data.get("email")
            user.first_name = miForm.cleaned_data.get("first_name")
            user.last_name = miForm.cleaned_data.get("last_name")
            user.save()
            return redirect(reverse_lazy('index'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = UserEditForm(instance=usuario)

    return render(request, "aplication/edit_profile.html", {"form": miForm} )    
   
class CambiarClave(LoginRequiredMixin, PasswordChangeView):
    template_name = "aplication/cambiar_clave.html"
    success_url = reverse_lazy("index")

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)

        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)
            #___ Borrar avatares viejos
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            #____________________________________________________
            avatar = Avatar(user=usuario,
                            imagen=miForm.cleaned_data["imagen"])
            avatar.save()
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen
            
            return redirect(reverse_lazy('index'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = AvatarForm()

    return render(request, "aplication/agregar_avatar.html", {"form": miForm} ) 

    
    