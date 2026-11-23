import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from proyectos.models import Proyecto
from .models import Categoria

MEDIA_TEMPORAL = tempfile.mkdtemp()


def imagen_de_prueba():
    archivo = BytesIO()
    Image.new('RGB', (10, 10), 'blue').save(archivo, 'PNG')
    return SimpleUploadedFile('prueba.png', archivo.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class CategoriasTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Backend')

    def test_el_listado_muestra_las_categorias(self):
        respuesta = self.client.get(reverse('categorias:lista'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Backend')

    def test_crear_una_categoria(self):
        respuesta = self.client.post(reverse('categorias:crear'), {'nombre': 'Frontend'})
        self.assertRedirects(respuesta, reverse('categorias:lista'))
        self.assertTrue(Categoria.objects.filter(nombre='Frontend').exists())

    def test_editar_una_categoria(self):
        self.client.post(reverse('categorias:editar', args=[self.categoria.id]), {'nombre': 'Back-end'})
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Back-end')

    def test_eliminar_una_categoria_borra_sus_proyectos(self):
        Proyecto.objects.create(
            titulo='API', descripcion='Prueba', imagen=imagen_de_prueba(), categoria=self.categoria
        )
        self.client.post(reverse('categorias:eliminar', args=[self.categoria.id]))
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())
        self.assertEqual(Proyecto.objects.count(), 0)
