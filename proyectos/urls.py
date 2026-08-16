from django.urls import path
from . import views

app_name = 'proyectos'

urlpatterns = [
    path('', views.lista_proyectos, name='lista'),
    path('crear/', views.crear_proyecto, name='crear'),
    path('editar/<int:id>/', views.editar_proyecto, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_proyecto, name='eliminar'),
]