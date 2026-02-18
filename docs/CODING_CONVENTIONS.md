# 📋 Convenciones de Código

Este documento establece las convenciones de código para el proyecto **Backend Furniture Store**.

---

## 📝 Estilo de Código

### Python Style Guide

Seguimos **PEP 8** como guía base de estilo. Utilizamos **Black** como formateador automático.

```bash
# Formatear código
black .

# Verificar estilo sin modificar
black --check .
```

### Configuración de Black

```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | __pycache__
  | migrations
)/
'''
```

---

## 📁 Convenciones de Nombres

### Archivos y Carpetas

| Tipo           | Convención | Ejemplo           |
|----------------|------------|-------------------|
| Módulos Python | snake_case | `user_service.py` |
| Carpetas       | snake_case | `wood_types/`     |
| Clases         | PascalCase | `ColorService`    |

### Variables y Funciones

| Tipo             | Convención       | Ejemplo             |
|------------------|------------------|---------------------|
| Variables        | snake_case       | `user_name`         |
| Funciones        | snake_case       | `get_all_colors()`  |
| Constantes       | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE`     |
| Clases           | PascalCase       | `ColorModel`        |
| Métodos privados | _snake_case      | `_validate_input()` |

### Modelos de Base de Datos

```python
class Color(db.Model):
    """
    Modelo de Color para el catálogo.
    
    Attributes:
        id: Identificador único
        name: Nombre del color
        hex_code: Código hexadecimal del color
        is_active: Estado activo/inactivo
    """
    __tablename__ = 'colors'  # Plural, snake_case

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    hex_code = db.Column(db.String(7), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
```

---

## 🏗️ Estructura de Módulos

### Estructura de un Módulo de Dominio

```
catalogs/
└── colors/
    ├── __init__.py      # Blueprint y exports
    ├── routes.py        # Rutas y controladores
    └── services.py      # Lógica de negocio

templates/
└── colors/
    └── list.html        # Vista del módulo
```

### Contenido de `__init__.py`

```python
"""
Módulo de gestión de colores.

Proporciona endpoints para CRUD de colores del catálogo.
"""

from flask import Blueprint

colors_bp = Blueprint('colors', __name__)

from . import routes  # noqa: E402, F401
```

### Contenido de `routes.py`

```python
"""
Rutas/Controladores para el módulo de colores.
"""

from flask import flash, redirect, render_template, request, url_for

from . import colors_bp
from .services import ColorService
from app.exceptions import ConflictError, ValidationError


@colors_bp.route('/', methods=['GET'])
def list_colors():
    """
    Muestra la lista de colores del catálogo.
    
    Returns:
        HTML: Página con la lista de colores
    """
    colors = ColorService.get_all()
    return render_template('colors/list.html', colors=colors)


@colors_bp.route('/', methods=['POST'])
def create_color():
    """
    Crea un nuevo color desde formulario.
    
    Form Data:
        name: Nombre del color
        
    Returns:
        Redirect: Redirige a la lista de colores
    """
    data = {'name': request.form.get('name')}
    try:
        ColorService.create(data)
        flash('Color creado exitosamente', 'success')
    except (ValidationError, ConflictError) as e:
        flash(e.message, 'error')
    return redirect(url_for('colors.list_colors'))
```

### Contenido de `services.py`

```python
"""
Servicios de lógica de negocio para colores.
"""

from app.models.color import Color
from app.extensions import db
from app.exceptions import ConflictError, ValidationError


class ColorService:
    """Servicio para operaciones de negocio relacionadas con colores."""

    @staticmethod
    def get_all() -> list:
        """
        Obtiene todos los colores activos.
        
        Returns:
            list: Lista de objetos Color activos
        """
        return Color.query.filter_by(active=True).all()

    @staticmethod
    def create(data: dict) -> dict:
        """
        Crea un nuevo color.
        
        Args:
            data: Diccionario con los datos del color
            
        Returns:
            dict: Color creado serializado
            
        Raises:
            ValidationError: Si el nombre está vacío
            ConflictError: Si el color ya existe
        """
        name = data.get('name')
        if not name or not name.strip():
            raise ValidationError('El nombre del color es requerido')

        existing = Color.query.filter_by(name=name.strip()).first()
        if existing:
            raise ConflictError(f"Ya existe un color con el nombre '{name}'")

        color = Color(name=name.strip())
        db.session.add(color)
        db.session.commit()
        return color.to_dict()
```

---

## 📚 Documentación

### Docstrings

Utilizamos el formato **Google Style** para docstrings:

```python
from typing import Optional

def create_color(name: str, hex_code: Optional[str] = None) -> dict:
    """
    Crea un nuevo color en el catálogo.
    
    Args:
        name: Nombre del color (requerido)
        hex_code: Código hexadecimal del color (opcional)
        
    Returns:
        dict: Color creado serializado
        
    Raises:
        ValidationError: Si el nombre está vacío
        ConflictError: Si el color ya existe
        
    Example:
        >>> create_color("Rojo", "#FF0000")
        {'id': 1, 'name': 'Rojo', 'hex_code': '#FF0000'}
    """
    pass
```

### Type Hints

Usar type hints en todas las funciones:

```python
from typing import List, Optional, Dict, Any


def get_colors_by_status(is_active: bool = True) -> List[Dict[str, Any]]:
    """Obtiene colores filtrados por estado."""
    pass


def find_color(color_id: int) -> Optional[Color]:
    """Busca un color, retorna None si no existe."""
    pass
```

---

## 🌐 Convenciones de Rutas y Vistas

### URLs

| Acción     | Método | URL                       | Ejemplo            |
|------------|--------|---------------------------|--------------------|   
| Listar     | GET    | `/{recurso}/`             | `/colors/`         |
| Crear      | POST   | `/{recurso}/`             | `/colors/`         |
| Detalle    | GET    | `/{recurso}/{id}`         | `/colors/1`        |
| Editar     | POST   | `/{recurso}/{id}/edit`    | `/colors/1/edit`   |
| Eliminar   | POST   | `/{recurso}/{id}/delete`  | `/colors/1/delete` |

### Templates Jinja2

#### Template Base (`base.html`)

Todos los templates extienden de `base.html` que contiene:
- Estructura HTML común
- Navegación
- Bloque de mensajes flash
- Bloque `content` para contenido específico

```html
{%- raw %}
{% extends "base.html" %}
{% block title %}Título - Furniture Store{% endblock %}
{% block content %}
    <!-- Contenido específico -->
{% endblock %}
{%- endraw %}
```

#### Organización de Templates

```
templates/
├── base.html              # Layout base
└── colors/                # Templates por módulo
    └── list.html          # Listado + formulario
```

#### Mensajes Flash

Se usa `flash()` para retroalimentación al usuario:

```python
# En routes.py
flash('Color creado exitosamente', 'success')  # Mensaje de éxito
flash(e.message, 'error')                      # Mensaje de error
```

#### Patrón PRG (Post/Redirect/Get)

Después de un POST exitoso, siempre redirigir:

```python
return redirect(url_for('colors.list_colors'))
```

---

## 🔢 Códigos HTTP

| Código | Uso                                        |
|--------|--------------------------------------------|
| 200    | OK - Operación exitosa                     |
| 201    | Created - Recurso creado                   |
| 204    | No Content - Eliminación exitosa           |
| 400    | Bad Request - Error de validación          |
| 401    | Unauthorized - No autenticado              |
| 403    | Forbidden - Sin permisos                   |
| 404    | Not Found - Recurso no encontrado          |
| 409    | Conflict - Conflicto (duplicado)           |
| 422    | Unprocessable Entity - Error de negocio    |
| 500    | Internal Server Error - Error del servidor |

---

## 🧪 Convenciones de Testing

### Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidos
├── test_config.py           # Tests de configuración
└── catalogs/
    └── test_colors.py       # Tests del módulo colors
```

### Nomenclatura de Tests

```python
def test_list_colors_renders_template():
    """Test: GET /colors/ renderiza la página de colores."""
    pass


def test_create_color_with_valid_data_redirects():
    """Test: POST /colors/ con datos válidos redirige a la lista."""
    pass


def test_create_color_duplicate_shows_error_flash():
    """Test: POST /colors/ con nombre duplicado muestra flash de error."""
    pass
```

---

## 📦 Imports

### Orden de Imports

1. Librerías estándar de Python
2. Librerías de terceros
3. Imports locales de la aplicación

```python
# 1. Librerías estándar
from datetime import datetime
from typing import List, Optional

# 2. Librerías de terceros
from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import or_, and_

# 3. Imports locales
from app.extensions import db
from app.models.color import Color
from app.exceptions import ConflictError, ValidationError
```

---

## ✅ Checklist de Revisión de Código

- [ ] El código sigue PEP 8 (formateado con Black)
- [ ] Todas las funciones tienen docstrings
- [ ] Se usan type hints
- [ ] Los nombres son descriptivos y siguen las convenciones
- [ ] Las excepciones se manejan correctamente
- [ ] Las rutas usan flash messages para retroalimentación
- [ ] Los templates extienden de `base.html`
- [ ] Se aplica el patrón PRG después de POST
- [ ] No hay código comentado innecesario
- [ ] Los imports están ordenados correctamente

