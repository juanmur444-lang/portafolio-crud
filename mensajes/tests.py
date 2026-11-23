from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Mensaje


class MensajesTests(TestCase):

    def datos_validos(self, **cambios):
        datos = {
            'nombre': 'Carlos Pérez',
            'correo': 'carlos@example.com',
            'telefono': '3000000000',
            'mensaje': 'Me interesa tu trabajo.',
        }
        datos.update(cambios)
        return datos

    def test_enviar_un_mensaje_valido_lo_guarda_y_muestra_gracias(self):
        respuesta = self.client.post(reverse('mensajes:enviar'), self.datos_validos())
        self.assertRedirects(respuesta, reverse('mensajes:gracias'))
        self.assertEqual(Mensaje.objects.count(), 1)

    def test_un_correo_invalido_no_se_guarda(self):
        self.client.post(reverse('mensajes:enviar'), self.datos_validos(correo='correo-malo'))
        self.assertEqual(Mensaje.objects.count(), 0)

    def test_un_mensaje_vacio_no_se_guarda(self):
        self.client.post(reverse('mensajes:enviar'), self.datos_validos(mensaje=''))
        self.assertEqual(Mensaje.objects.count(), 0)

    def test_el_visitante_no_puede_ver_los_mensajes(self):
        respuesta = self.client.get(reverse('mensajes:lista'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/admin/login/', respuesta.url)

    def test_el_administrador_puede_ver_los_mensajes(self):
        Mensaje.objects.create(**self.datos_validos())
        admin = User.objects.create_user('admin', password='clave-de-prueba-123', is_staff=True)
        self.client.force_login(admin)
        respuesta = self.client.get(reverse('mensajes:lista'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Carlos Pérez')
