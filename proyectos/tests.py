import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from categorias.models import Categoria
from .models import Proyecto

# Las imágenes de las pruebas se guardan en una carpeta temporal que se borra al final
MEDIA_TEMPORAL = tempfile.mkdtemp()


def imagen_de_prueba(nombre='prueba.png'):
    """Crea una imagen PNG pequeña en memoria para subirla en el formulario."""
    archivo = BytesIO()
    Image.new('RGB', (10, 10), 'blue').save(archivo, 'PNG')
    return SimpleUploadedFile(nombre, archivo.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class ProyectosTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Backend')
        self.proyecto = Proyecto.objects.create(
            titulo='API de tareas',
            descripcion='API REST para gestionar tareas.',
            imagen=imagen_de_prueba(),
            categoria=self.categoria,
        )

    def datos(self, **cambios):
        datos = {
            'titulo': 'Portafolio',
            'descripcion': 'Mi sitio personal.',
            'enlace': 'https://github.com/juanmur444-lang',
            'categoria': self.categoria.id,
            'imagen': imagen_de_prueba('portafolio.png'),
        }
        datos.update(cambios)
        return datos

    def test_la_raiz_lleva_a_la_pagina_de_inicio(self):
        respuesta = self.client.get('/', follow=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'proyectos/inicio.html')

    def test_el_listado_muestra_los_proyectos(self):
        respuesta = self.client.get(reverse('proyectos:lista'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'API de tareas')

    def test_crear_un_proyecto(self):
        respuesta = self.client.post(reverse('proyectos:crear'), self.datos())
        self.assertRedirects(respuesta, reverse('proyectos:lista'))
        self.assertTrue(Proyecto.objects.filter(titulo='Portafolio').exists())

    def test_el_enlace_es_opcional(self):
        self.client.post(reverse('proyectos:crear'), self.datos(enlace=''))
        self.assertTrue(Proyecto.objects.filter(titulo='Portafolio').exists())

    def test_un_enlace_invalido_no_se_guarda(self):
        respuesta = self.client.post(reverse('proyectos:crear'), self.datos(enlace='esto no es un enlace'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Proyecto.objects.filter(titulo='Portafolio').exists())

    def test_la_imagen_es_obligatoria(self):
        datos = self.datos()
        datos.pop('imagen')
        self.client.post(reverse('proyectos:crear'), datos)
        self.assertFalse(Proyecto.objects.filter(titulo='Portafolio').exists())

    def test_un_archivo_que_no_es_imagen_no_se_acepta(self):
        texto = SimpleUploadedFile('nota.txt', b'hola', content_type='text/plain')
        self.client.post(reverse('proyectos:crear'), self.datos(imagen=texto))
        self.assertFalse(Proyecto.objects.filter(titulo='Portafolio').exists())

    def test_editar_un_proyecto_sin_cambiar_la_imagen(self):
        self.client.post(reverse('proyectos:editar', args=[self.proyecto.id]), {
            'titulo': 'API de tareas v2',
            'descripcion': self.proyecto.descripcion,
            'categoria': self.categoria.id,
        })
        self.proyecto.refresh_from_db()
        self.assertEqual(self.proyecto.titulo, 'API de tareas v2')

    def test_eliminar_con_get_solo_pide_confirmacion(self):
        respuesta = self.client.get(reverse('proyectos:eliminar', args=[self.proyecto.id]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(Proyecto.objects.filter(id=self.proyecto.id).exists())

    def test_eliminar_con_post_borra_el_proyecto(self):
        respuesta = self.client.post(reverse('proyectos:eliminar', args=[self.proyecto.id]))
        self.assertRedirects(respuesta, reverse('proyectos:lista'))
        self.assertFalse(Proyecto.objects.filter(id=self.proyecto.id).exists())

    def test_un_proyecto_que_no_existe_da_404(self):
        respuesta = self.client.get(reverse('proyectos:editar', args=[9999]))
        self.assertEqual(respuesta.status_code, 404)
