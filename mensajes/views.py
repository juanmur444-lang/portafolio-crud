from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Mensaje
from .forms import MensajeForm


def enviar_mensaje(peticion):
    if peticion.method == 'POST':
        formulario = MensajeForm(peticion.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('mensajes:gracias')
    return redirect('proyectos:lista')


def gracias(peticion):
    return render(peticion, 'mensajes/gracias.html')


@staff_member_required(login_url='/admin/login/')
def lista_mensajes(peticion):
    mensajes = Mensaje.objects.all().order_by('-fecha_envio')
    return render(peticion, 'mensajes/lista.html', {'mensajes': mensajes})