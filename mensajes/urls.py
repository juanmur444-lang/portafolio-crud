from django.urls import path
from . import views

app_name = 'mensajes'

urlpatterns = [
    path('enviar/', views.enviar_mensaje, name='enviar'),
    path('gracias/', views.gracias, name='gracias'),
    path('', views.lista_mensajes, name='lista'),
]