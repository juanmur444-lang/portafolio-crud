from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto
from .forms import ProyectoForm


def lista_proyectos(peticion):
    proyectos = Proyecto.objects.select_related('categoria').all()
    return render(peticion, 'proyectos/lista.html', {'proyectos': proyectos})


def crear_proyecto(peticion):
    if peticion.method == 'POST':
        formulario = ProyectoForm(peticion.POST, peticion.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('proyectos:lista')
    else:
        formulario = ProyectoForm()
    return render(peticion, 'proyectos/formulario.html', {'formulario': formulario, 'titulo': 'Crear proyecto'})


def editar_proyecto(peticion, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    if peticion.method == 'POST':
        formulario = ProyectoForm(peticion.POST, peticion.FILES, instance=proyecto)
        if formulario.is_valid():
            formulario.save()
            return redirect('proyectos:lista')
    else:
        formulario = ProyectoForm(instance=proyecto)
    return render(peticion, 'proyectos/formulario.html', {'formulario': formulario, 'titulo': 'Editar proyecto'})


def eliminar_proyecto(peticion, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    if peticion.method == 'POST':
        proyecto.delete()
        return redirect('proyectos:lista')
    return render(peticion, 'proyectos/eliminar.html', {'proyecto': proyecto})