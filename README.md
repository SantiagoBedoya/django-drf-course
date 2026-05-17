# django-course

Repositorio personal de aprendizaje de Django. Contiene tres proyectos independientes que cubren desde los fundamentos del framework hasta la construcción de APIs REST y aplicaciones web completas.

## Proyectos

### 1. `my_first_project/` — Introducción a Django

Primer contacto con Django 6.0.5. Proyecto didáctico que explora los conceptos esenciales del framework:

- Modelos, migraciones y relaciones (ForeignKey, ManyToManyField, OneToOneField)
- Vistas basadas en clases (TemplateView) y vistas basadas en funciones
- Captura de parámetros en URLs (`<int:id>`, `<str:brand>`)
- Templates y herencia
- Evolución incremental del modelo de datos a través de 6 migraciones

### 2. `coffee_shop/` — Aplicación web de tienda de café

Aplicación Django funcional para la gestión de una cafetería. Demuestra el flujo completo de una aplicación real:

- **Catálogo de productos**: listado y carga de productos con imágenes
- **Autenticación de usuarios**: login/logout con el sistema de auth de Django
- **Órdenes de compra**: carrito de compras activo por usuario (orden → productos)
- **API REST**: endpoint JSON con Django REST Framework
- **Panel de administración**: admin personalizado con búsqueda e inlines
- **Testing**: pruebas unitarias con TestCase y Client

### 3. `django_rest_framework/` — API REST de gestión médica

API completa para la gestión de citas médicas construida con Django REST Framework. Implementa **dos estilos arquitectónicos en paralelo** con fines didácticos:

- **ViewSets + DefaultRouter** (automático) y **Generic Class-Based Views** (explícito)
- 9 modelos distribuidos en 3 apps: doctores, pacientes y reservas
- Serializers con validación (field-level y object-level), nested serializers y SerializerMethodField
- Permisos personalizados (IsDoctor por grupos) y autenticación por sesión
- Throttling (anónimo 5 req/min, usuario 1000 req/min)
- Documentación automática con drf-spectacular (Swagger UI + ReDoc)
- Suite de tests de 746 líneas para la app de doctores

## Requisitos

- Python >= 3.14
- Django >= 6.0.5
- Cada proyecto tiene su propio `pyproject.toml` y entorno virtual con `uv`

## Uso

```bash
cd <proyecto>
uv run python manage.py runserver
```

Cada proyecto incluye su propio `README.md` con documentación detallada de los conceptos cubiertos.
