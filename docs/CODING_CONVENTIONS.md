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
    ├── routes.py        # Endpoints de la API
    ├── services.py      # Lógica de negocio
    └── schemas.py       # Validación de datos (opcional)
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
Rutas/Endpoints para el módulo de colores.
"""

from flask import request
from . import colors_bp
from .services import ColorService
from app.utils.responses import success_response, error_response


@colors_bp.route('/', methods=['GET'])
def get_all_colors():
    """
    Obtiene todos los colores del catálogo.
    
    Returns:
        JSON: Lista de colores
    """
    colors = ColorService.get_all()
    return success_response(data=colors, message="Colores obtenidos exitosamente")


@colors_bp.route('/<int:color_id>', methods=['GET'])
def get_color(color_id: int):
    """
    Obtiene un color por su ID.
    
    Args:
        color_id: ID del color
        
    Returns:
        JSON: Datos del color
    """
    color = ColorService.get_by_id(color_id)
    return success_response(data=color)
```

### Contenido de `services.py`

```python
"""
Servicios de lógica de negocio para colores.
"""

from app.models.color import Color
from app.extensions import db
from app.exceptions import NotFoundError, ValidationError


class ColorService:
    """Servicio para operaciones de negocio relacionadas con colores."""

    @staticmethod
    def get_all() -> list:
        """
        Obtiene todos los colores activos.
        
        Returns:
            list: Lista de colores serializados
        """
        colors = Color.query.filter_by(is_active=True).all()
        return [color.to_dict() for color in colors]

    @staticmethod
    def get_by_id(color_id: int) -> dict:
        """
        Obtiene un color por su ID.
        
        Args:
            color_id: ID del color
            
        Returns:
            dict: Color serializado
            
        Raises:
            NotFoundError: Si el color no existe
        """
        color = Color.query.get(color_id)
        if not color:
            raise NotFoundError(f"Color con ID {color_id} no encontrado")
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

## 🌐 Convenciones de API REST

### URLs

| Acción     | Método | URL                       | Ejemplo            |
|------------|--------|---------------------------|--------------------|
| Listar     | GET    | `/api/v1/{recursos}`      | `/api/v1/colors`   |
| Obtener    | GET    | `/api/v1/{recursos}/{id}` | `/api/v1/colors/1` |
| Crear      | POST   | `/api/v1/{recursos}`      | `/api/v1/colors`   |
| Actualizar | PUT    | `/api/v1/{recursos}/{id}` | `/api/v1/colors/1` |
| Eliminar   | DELETE | `/api/v1/{recursos}/{id}` | `/api/v1/colors/1` |

### Respuestas JSON

#### Respuesta Exitosa

```json
{
  "success": true,
  "message": "Color creado exitosamente",
  "data": {
    "id": 1,
    "name": "Rojo",
    "hex_code": "#FF0000"
  }
}
```

#### Respuesta de Error

```json
{
  "success": false,
  "error": {
    "message": "Color no encontrado",
    "code": 404,
    "details": {
      "color_id": 999
    }
  }
}
```

#### Respuesta Paginada

```json
{
  "success": true,
  "message": "Colores obtenidos exitosamente",
  "data": [
    ...
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 50,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
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
def test_get_all_colors_returns_list():
    """Test: GET /colors retorna lista de colores."""
    pass


def test_get_color_by_id_not_found_returns_404():
    """Test: GET /colors/{id} retorna 404 si no existe."""
    pass


def test_create_color_with_valid_data_returns_201():
    """Test: POST /colors con datos válidos retorna 201."""
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
from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_

# 3. Imports locales
from app.extensions import db
from app.models.color import Color
from app.exceptions import NotFoundError
from app.utils.responses import success_response
```

---

## ✅ Checklist de Revisión de Código

- [ ] El código sigue PEP 8 (formateado con Black)
- [ ] Todas las funciones tienen docstrings
- [ ] Se usan type hints
- [ ] Los nombres son descriptivos y siguen las convenciones
- [ ] Las excepciones se manejan correctamente
- [ ] Los endpoints usan las respuestas estandarizadas
- [ ] No hay código comentado innecesario
- [ ] Los imports están ordenados correctamente

