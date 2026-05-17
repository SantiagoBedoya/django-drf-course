# My First Project

Proyecto Django creado con Django 6.0.5 y Python 3.14.

---

## Conceptos de Django usados en este proyecto

### 1. Proyecto vs App (`my_first_project/` y `my_first_app/`)

- **Proyecto**: es el sitio web completo — la configuración global, URLs raíz, settings. Se crea con `django-admin startproject`.
- **App**: es un módulo dentro del proyecto que hace una cosa específica (ej: gestionar carros, libros, autores). Se crea con `python manage.py startapp`.

En este proyecto tenemos 1 proyecto y 1 app.

---

### 2. `manage.py`

Herramienta de línea de comandos para administrar el proyecto. Sirve para correr el servidor, crear migraciones, crear apps, etc.

```bash
python manage.py runserver        # Inicia el servidor de desarrollo
python manage.py makemigrations   # Crea migraciones basadas en cambios a models.py
python manage.py migrate          # Aplica migraciones a la base de datos
python manage.py startapp <nombre># Crea una nueva app
```

---

### 3. `settings.py` (`my_first_project/settings.py`)

Archivo de configuración central del proyecto. Define:
- `INSTALLED_APPS`: qué apps están instaladas (incluye `my_first_app`).
- `DATABASES`: qué base de datos usar (SQLite en este caso).
- `MIDDLEWARE`: componentes que procesan cada request/response.
- `TEMPLATES`: configuración del motor de plantillas.
- `LANGUAGE_CODE`, `TIME_ZONE`: configuración regional.
- `STATIC_URL`: ruta para archivos estáticos (CSS, JS, imágenes).
- `SECRET_KEY`: clave secreta para firmar cookies y sesiones (¡nunca compartir!).
- `DEBUG`: modo de desarrollo (`True` = muestra errores detallados).

---

### 4. URLs (`urls.py`)

Sistema de ruteo que mapea URLs a vistas.

**A nivel del proyecto** (`my_first_project/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),        # /admin/ → admin de Django
    path("cars/", include('my_first_app.urls'))  # /cars/... → delega a la app
]
```

**A nivel de la app** (`my_first_app/urls.py`):
```python
urlpatterns = [
    path("list/", CarListView.as_view()),                          # /cars/list/
    path("detail/<int:car_id>", my_test_view),                    # /cars/detail/5
    path("brands/<str:brand>", my_test_view)                      # /cars/brands/Toyota
]
```

Los **capturadores** (`<int:car_id>`, `<str:brand>`) extraen valores de la URL y los pasan a la vista como argumentos.

---

### 5. Vistas (`views.py`)

Son funciones o clases que reciben un request HTTP y devuelven un response.

**Function-Based View (FBV)** — vista como función:
```python
def my_test_view(request, *args, **kwargs):
    return HttpResponse("")
```

**Class-Based View (CBV)** — vista como clase. En este proyecto se usa `TemplateView`:
```python
class CarListView(TemplateView):
    template_name = "my_first_app/car_list.html"

    def get_context_data(self):
        return {"car_list": Car.objects.all()}
```

`TemplateView` es una vista genérica que solo renderiza un template. `get_context_data()` inyecta datos en el template.

---

### 6. Modelos (`models.py`)

Los modelos son clases de Python que representan tablas en la base de datos. Django ORM traduce automáticamente operaciones en Python a SQL.

**Modelos definidos**:

| Modelo      | Tabla en BD          | Campos                                                                 |
|-------------|----------------------|------------------------------------------------------------------------|
| `Car`       | `my_first_app_car`   | `title`, `year`, `color`                                               |
| `Publisher` | `my_first_app_publisher` | `name`, `address`                                                   |
| `Author`    | `my_first_app_author`| `name`, `birth_date`                                                   |
| `Book`      | `my_first_app_book`  | `title`, `publication_date`, `publisher` (FK), `authors` (M2M)         |
| `Profile`   | `my_first_app_profile`| `author` (OneToOne), `website`, `biography`                          |

**Tipos de campo usados**:
- `TextField` — texto (con `max_length` opcional)
- `DateField` — fecha
- `URLField` — URL válida
- `IntegerField`, `CharField`, etc. (no usados acá pero comunes)

---

### 7. Relaciones entre modelos

Django soporta tres tipos de relaciones:

- **`ForeignKey`** — Muchos-a-uno (Many-to-One). Ej: un `Publisher` puede tener muchos `Book`s, cada `Book` pertenece a un `Publisher`.
  ```python
  publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
  ```

- **`ManyToManyField`** — Muchos-a-muchos (Many-to-Many). Ej: un `Book` puede tener varios `Author`s y un `Author` puede escribir varios `Book`s.
  ```python
  authors = models.ManyToManyField(Author, related_name="authors")
  ```

- **`OneToOneField`** — Uno-a-uno (One-to-One). Ej: cada `Author` tiene exactamente un `Profile`.
  ```python
  author = models.OneToOneField(Author, on_delete=models.CASCADE)
  ```

**`on_delete=models.CASCADE`**: si se borra el registro padre, se borran también los hijos.

**`related_name`**: nombre para navegar la relación en sentido inverso (ej: `author.book_set` sin `related_name`, o `author.authors` con él).

---

### 8. Migraciones (`migrations/`)

Archivos que registran cambios en los modelos para sincronizar la base de datos.

Flujo de trabajo:
1. Se edita `models.py` (se agrega un campo, un modelo nuevo, etc.)
2. `python manage.py makemigrations` — genera el archivo de migración
3. `python manage.py migrate` — aplica los cambios a la base de datos

En este proyecto hay 6 migraciones que construyen el esquema paso a paso:
1. `0001_initial` — crea el modelo `Car` con `title`
2. `0002_car_year` — agrega `year` a `Car`
3. `0003_car_color` — agrega `color` a `Car`
4. `0004_publisher_book` — crea `Publisher` y `Book` (con FK a Publisher)
5. `0005_author_book_authors` — crea `Author` y agrega M2M a `Book`
6. `0006_profile` — crea `Profile` (con OneToOne a Author)

---

### 9. Templates (`templates/`)

Archivos HTML con sintaxis especial de Django (Django Template Language) para mostrar datos dinámicos.

En este proyecto: `my_first_app/templates/my_first_app/car_list.html`

```html
<ul>
    {% for car in car_list %}
    <li>{{car.title}}</li>
    {% endfor %}
</ul>
```

- `{{ variable }}` — imprime el valor de una variable
- `{% for ... %}` — bucle
- `{% if ... %}` — condicional
- `{% block %}`, `{% extends %}` — herencia de templates (no usado acá)

Django busca templates dentro de cada app en el directorio `templates/` (`APP_DIRS=True`).

---

### 10. Admin de Django (`admin.py`)

Interfaz administrativa automática. Para usarla:
1. Crear un superusuario: `python manage.py createsuperuser`
2. Ir a `/admin/` en el navegador
3. Registrar modelos en `admin.py` para gestionarlos desde el panel

En este proyecto el `admin.py` está vacío — ningún modelo está registrado aún.

---

### 11. ORM (Object-Relational Mapping)

Django traduce código Python a SQL automáticamente. Ejemplos de consultas:

```python
Car.objects.all()                    # SELECT * FROM my_first_app_car
Car.objects.filter(year="2020")      # SELECT ... WHERE year = '2020'
Car.objects.get(id=1)                # SELECT ... WHERE id = 1 (devuelve uno)
Car.objects.create(title="Tesla")    # INSERT INTO ...
```

---

### 12. WSGI y ASGI

Protocolos para servir Django en producción:

- **`wsgi.py`**: interfaz WSGI (Web Server Gateway Interface) — el estándar tradicional para aplicaciones Python web síncronas.
- **`asgi.py`**: interfaz ASGI (Asynchronous Server Gateway Interface) — soporta conexiones asíncronas y WebSockets.

Ambos archivos exponen una variable `application` que el servidor web (Gunicorn, uWSGI, Daphne) usa para comunicarse con Django.

---

### 13. Middleware

Componentes que procesan cada request antes de llegar a la vista y cada response antes de llegar al cliente. Se configuran en `settings.py` > `MIDDLEWARE`.

Ejemplos incluidos por defecto:
- `SecurityMiddleware` — seguridad (HTTPS, etc.)
- `SessionMiddleware` — manejo de sesiones
- `CsrfViewMiddleware` — protección contra CSRF
- `AuthenticationMiddleware` — asocia el usuario logueado al request

---

### 14. Base de datos SQLite

Esta tabla `.gitignore` da las rutas relevantes.
Django está configurado con SQLite (`ENGINE: django.db.backends.sqlite3`), que guarda todo en un solo archivo (`db.sqlite3`). Es ideal para desarrollo, no para producción.

---

### 15. Método `__str__` en modelos

Define cómo se representa un objeto como texto:

```python
def __str__(self):
    return f"{self.title} - {self.year}"
```

Esto se usa en el admin de Django y en el shell (`python manage.py shell`).

---

### 16. Shell de Django

```bash
python manage.py shell
```

Abre una consola interactiva de Python con acceso a los modelos y la base de datos. Se puede usar para probar consultas ORM, crear datos de prueba, etc.
