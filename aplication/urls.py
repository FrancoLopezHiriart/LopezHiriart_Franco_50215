from django.urls import path, include
from .views import *
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    #__________________ Generales

    path('', home, name= "home"),
    path('buscar_equipos/', buscarEquipos, name="buscar_equipos"),
    path('encontrar_equipos/', encontrarEquipos, name="encontrar_equipos"),
    path('acerca_de_mi/', acerca, name="acerca_de_mi"),
           
    #___________________ Equipos

    path('equipos/', EquipoList.as_view(), name="equipos"), 
    path('equipos_create/', EquipoCreate.as_view(), name="equipos_create"), 
    path('equipos_update/<int:pk>/', EquipoUpdate.as_view(), name="equipos_update"), 
    path('equipos_delete/<int:pk>/', EquipoDelete.as_view(), name="equipos_delete"), 

    #___________________ Jugadores

    path('jugadores/', JugadorList.as_view(), name="jugadores"), 
    path('jugadores_create/', JugadorCreate.as_view(), name="jugadores_create"), 
    path('jugadores_update/<int:pk>/', JugadorUpdate.as_view(), name="jugadores_update"), 
    path('jugadores_delete/<int:pk>/', JugadorDelete.as_view(), name="jugadores_delete"), 

    #___________________ Directores Tecnicos

    path('directores_tecnicos/', DirectorTecnicoList.as_view(), name="directores_tecnicos"), 
    path('directores_tecnicos_create/', DirectorTecnicoCreate.as_view(), name="directores_tecnicos_create"), 
    path('directores_tecnicos_update/<int:pk>/', DirectorTecnicoUpdate.as_view(), name="directores_tecnicos_update"), 
    path('directores_tecnicos_delete/<int:pk>/', DirectorTecnicoDelete.as_view(), name="directores_tecnicos_delete"), 

    #___________________ Nuevos Talentos

    path('talentos/', TalentoList.as_view(), name="talentos"), 
    path('talentos_create/', TalentoCreate.as_view(), name="talentos_create"), 
    path('talentos_update/<int:pk>/', TalentoUpdate.as_view(), name="talentos_update"), 
    path('talentos_delete/<int:pk>/', TalentoDelete.as_view(), name="talentos_delete"), 
    
    #___________________Registro y Autenticacion

    path('login/', login_request, name= "login"),
    path('logout/', LogoutView.as_view(), name= "logout"),
    path('registrar/', register, name="registrar"),

    #____________________ Edicion Perfil, Cambio de Clave, Avatar

    path('perfil/', editProfile, name="perfil"),
    path('<int:pk>/password/', CambiarClave.as_view(), name="cambiar_clave"),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"),
]   