# Coffee Shop

Proyecto Django para gestionar productos, órdenes y usuarios de una cafetería.

---

## Conceptos de Django usados en este proyecto

### 1. Proyecto y Apps

Django organiza el código en **proyectos** (el sitio completo) y **apps** (módulos con funcionalidad específica).

En este proyecto:
- **`coffee_shop/`** — proyecto principal. Contiene `settings.py` (configuración global) y `urls.py` (rutas raíz).
- **`products/`** — app para productos (nombre, precio, foto, etc.).
- **`users/`** — app para autenticación (login, logout).
- **`orders/`** — app para órdenes de compra.

---

### 2. Models (Modelos)

Los modelos son clases de Python que representan tablas en la base de datos. Cada atributo es una columna.

**`Product`** (`products/models.py`):
```python
class Product(models.Model):
    name = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="logos", null=True, blank=True)
```

**`Order`** y **`OrderProduct`** (`orders/models.py`): modelos relacionados con el usuario y los productos.

---

### 3. Field Types (Tipos de campos)

Cada tipo de campo define qué dato se guarda y cómo se valida:

| Campo | Uso |
|---|---|
| `TextField` | Texto corto/mediano |
| `DecimalField` | Números decimales (precios) |
| `BooleanField` | Verdadero/Falso |
| `ImageField` | Subida de imágenes |
| `DateTimeField` | Fecha y hora |
| `IntegerField` | Números enteros |
| `ForeignKey` | Relación con otro modelo |

---

### 4. Relaciones entre modelos (ForeignKey)

`ForeignKey` conecta un modelo con otro (relación muchos-a-uno).

- `Order.user → User`: una orden pertenece a un usuario. `on_delete=CASCADE` — si el usuario se elimina, su orden también.
- `OrderProduct.order → Order`: `CASCADE`.
- `OrderProduct.product → Product`: `on_delete=PROTECT` — no se puede eliminar un producto si está en alguna orden.

---

### 5. Migrations

Django genera automáticamente archivos de migración que aplican cambios al esquema de la base de datos.

Comandos:
```bash
python manage.py makemigrations   # crea migraciones
python manage.py migrate          # las ejecuta
```

Las migraciones están en `products/migrations/` y `orders/migrations/`.

---

### 6. Admin Interface

Django genera un panel de administración automáticamente. Se configura en `admin.py`:

- **`ProductAdmin`**: muestra `name` y `price` en la lista, permite buscar por nombre.
- **`OrderAdmin`**: muestra las líneas de la orden en línea (inline) con `OrderProductInlineAdmin`.

---

### 7. URL Routing

Las URLs se definen con `path()` y se pueden agrupar con `include()`.

```python
# coffee_shop/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('users/', include('users.urls')),
    path('orders/', include('orders.urls')),
]
```

Cada app tiene su propio `urls.py` con rutas específicas. Las rutas pueden tener un **nombre** (`name='list_product'`) para referenciarlas en templates y vistas.

---

### 8. Class-Based Views (Vistas basadas en clases)

Django provee vistas genéricas que evitan escribir código repetitivo:

- **`ListView`** — lista objetos de un modelo (`ProductListView`).
- **`DetailView`** — muestra un objeto específico (`MyOrderView`).
- **`FormView`** — muestra y procesa un formulario (`ProductFormView`).
- **`CreateView`** — crea un objeto con un formulario (`CreateOrderProductView`).
- **`LoginView`** / **`LogoutView`** — vistas de autenticación incorporadas.

También se usa **`LoginRequiredMixin`** para proteger vistas que requieren sesión iniciada.

---

### 9. Forms (Formularios)

Los formularios manejan entrada de datos, validación y (opcionalmente) guardado.

- **`forms.Form`** — formulario genérico (`ProductForm`). Tiene un método `save()` personalizado que crea el producto manualmente.
- **`ModelForm`** — formulario vinculado a un modelo (`OrderProductForm`). Genera campos automáticamente y se conecta al modelo.

---

### 10. Templates (Plantillas)

Django usa su propio motor de plantillas con herencia:

- **`base.html`** — plantilla base con header, Tailwind CSS, y un bloque `{% block content %}`.
- Las demás plantillas heredan con `{% extends "base.html" %}` y llenan el bloque.

Etiquetas de template usadas:
- `{% url 'name' %}` — genera una URL a partir de su nombre.
- `{% csrf_token %}` — protección contra CSRF en formularios.
- `{% for %}` / `{% if %}` / `{% empty %}` — lógica de control.
- `{{ variable|filter }}` — filtros como `|date`.

---

### 11. Autenticación

Django incluye un sistema completo de usuarios y sesiones:

- **`LoginView`** — muestra formulario de login y autentica al usuario.
- **`LogoutView`** — cierra sesión.
- **`LoginRequiredMixin`** — redirige al login si no hay sesión.
- **`LOGIN_URL`** y **`LOGIN_REDIRECT_URL`** — configurados en `settings.py`.

En los templates se usa `{{ user.is_authenticated }}` para mostrar contenido condicional.

---

### 12. Django REST Framework (DRF)

DRF permite crear APIs REST fácilmente:

- **`APIView`** — vista que devuelve JSON (`ProductListAPI`).
- **`ModelSerializer`** — convierte modelos a JSON automáticamente (`ProductSerializer`).
- **Permisos** — configuración global `DjangoModelPermissionsOrAnonReadOnly`.

---

### 13. Settings (Configuración)

`settings.py` contiene toda la configuración del proyecto:

- `INSTALLED_APPS` — lista de apps habilitadas.
- `MIDDLEWARE` — pipeline de procesamiento de requests.
- `DATABASES` — conexión a base de datos (SQLite por defecto).
- `TEMPLATES` — configuración del motor de plantillas.
- `STATIC_URL` / `MEDIA_URL` — URLs para archivos estáticos y media.
- `SECRET_KEY` / `DEBUG` / `ALLOWED_HOSTS` — seguridad y entorno.

---

### 14. Media Files (Archivos subidos)

`ImageField` guarda imágenes en una carpeta del servidor (`logos/`). Django sirve estos archivos en desarrollo si se configura `MEDIA_URL` y `MEDIA_ROOT`.

---

### 15. Tests

Django tiene un framework de testing basado en `unittest`:

```python
class ProductListViewTests(TestCase):
    def test_should_return_200(self):
        url = reverse('list_product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
```

Usa `TestCase`, `Client` (simula requests) y `reverse()` (genera URLs por nombre).

---

### 16. Middleware

El middleware son componentes que procesan cada request/response globalmente. En este proyecto se usan los 8 middleware por defecto de Django (seguridad, sesiones, autenticación, CSRF, etc.).

---

### 17. WSGI/ASGI

Archivos de configuración para desplegar Django en servidores:
- **`wsgi.py`** — interfaz tradicional (Apache, Gunicorn).
- **`asgi.py`** — interfaz asíncrona (Daphne, Uvicorn).

---

### 18. Context Processors

Funciones que inyectan variables en **todas** las plantillas. Las activas en este proyecto son:
- `django.template.context_processors.request` — agrega `request` al contexto.
- `django.contrib.auth.context_processors.auth` — agrega `user` y `perms`.
- `django.contrib.messages.context_processors.messages` — agrega mensajes flash.
