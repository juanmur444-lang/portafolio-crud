# Portafolio CRUD

Aplicación web hecha con Django para administrar los proyectos de un portafolio: permite crearlos, verlos en un listado, editarlos y eliminarlos, organizados por categorías. Incluye una sección de mensajes de contacto.

Práctica académica del Tecnólogo en Análisis y Desarrollo de Software (ADSO), SENA.

## Funcionalidades

- Página de inicio.
- Listado de proyectos con su categoría.
- Crear proyectos con título, descripción, imagen, enlace opcional y categoría.
- Editar un proyecto existente.
- Eliminar un proyecto, con página de confirmación.
- Gestión de categorías.
- Mensajes de contacto.

## Tecnologías

- Python
- Django
- HTML y CSS (plantillas de Django)

## Estructura

- `proyectos/`: modelo, formulario y vistas de los proyectos.
- `categorias/`: categorías a las que pertenece cada proyecto.
- `mensajes/`: mensajes del formulario de contacto.
- `portafolio_config/`: configuración general y rutas.

## Cómo ejecutarlo

```
git clone https://github.com/juanmur444-lang/portafolio-crud.git
cd portafolio-crud
pip install django pillow
python manage.py migrate
python manage.py runserver
```

Luego abre `http://127.0.0.1:8000` en el navegador.

## Qué aprendí

- Organizar un proyecto Django en varias aplicaciones.
- Relacionar modelos con una llave foránea (proyecto y categoría).
- Validar formularios y subir imágenes.
- Usar nombres de rutas con namespace para las redirecciones.

## Mejoras pendientes

- Agregar inicio de sesión para proteger la creación, edición y eliminación.

## Autor

Juan Andrés Mur Bermúdez · [github.com/juanmur444-lang](https://github.com/juanmur444-lang)
