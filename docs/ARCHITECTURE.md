# 🏗️ Arquitectura Base

Este documento describe la arquitectura base del proyecto **Backend Furniture Store**.

---

## 📐 Visión General

El proyecto implementa una **arquitectura en capas** (Layered Architecture) siguiendo los principios de separación de
responsabilidades y bajo acoplamiento.

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE                                 │
│                    (Frontend / Mobile)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API REST (Flask)                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Colors    │  │  Wood Types │  │  Furniture  │   ...        │
│  │   Module    │  │   Module    │  │   Module    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│                    CAPA DE SERVICIOS                            │
│              (Lógica de Negocio / Validaciones)                 │
├─────────────────────────────────────────────────────────────────┤
│                    CAPA DE MODELOS                              │
│                  (ORM SQLAlchemy)                               │
├─────────────────────────────────────────────────────────────────┤
│                    BASE DE DATOS                                │
│                       (MySQL)                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧱 Capas de la Arquitectura

### 1. Capa de Presentación (routes.py)

**Responsabilidad:** Manejar las peticiones HTTP y devolver respuestas JSON.

```python
# app/catalogs/colors/routes.py

@colors_bp.route('/', methods=['GET'])
def get_all_colors():
    """Endpoint para obtener todos los colores."""
    colors = ColorService.get_all()
    return success_response(data=colors)
```

**Características:**

- Define los endpoints REST de la API
- Valida parámetros de entrada básicos
- Delega la lógica de negocio a la capa de servicios
- Utiliza respuestas estandarizadas

---

### 2. Capa de Servicios (services.py)

**Responsabilidad:** Contener la lógica de negocio y orquestar operaciones.

```python
# app/catalogs/colors/services.py

class ColorService:
    @staticmethod
    def get_all() -> list:
        """Obtiene todos los colores activos."""
        colors = Color.query.filter_by(is_active=True).all()
        return [color.to_dict() for color in colors]

    @staticmethod
    def create(data: dict) -> dict:
        """Crea un nuevo color con validaciones de negocio."""
        # Validar que no exista un color con el mismo nombre
        existing = Color.query.filter_by(name=data['name']).first()
        if existing:
            raise ConflictError(f"Ya existe un color con el nombre '{data['name']}'")

        color = Color(**data)
        db.session.add(color)
        db.session.commit()
        return color.to_dict()
```

**Características:**

- Implementa reglas de negocio
- Maneja transacciones de base de datos
- Lanza excepciones específicas del dominio
- Es independiente del framework web

---

### 3. Capa de Modelos (models/)

**Responsabilidad:** Definir las entidades y su mapeo a la base de datos.

```python
# app/models/color.py

class Color(db.Model):
    """Modelo de Color para el catálogo."""

    __tablename__ = 'colors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    hex_code = db.Column(db.String(7))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serializa el modelo a diccionario."""
        return {
            'id': self.id,
            'name': self.name,
            'hex_code': self.hex_code,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

**Características:**

- Define la estructura de las tablas
- Implementa métodos de serialización
- Contiene relaciones entre entidades
- No contiene lógica de negocio

---

### 4. Capa de Configuración

**Responsabilidad:** Gestionar la configuración del entorno y extensiones.

```python
# config.py
class Config:
    """Configuración base de la aplicación."""
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    # ...


# app/extensions.py
db = SQLAlchemy()
migrate = Migrate()
```

---

## 🔄 Flujo de Datos

### Petición GET (Lectura)

```
Cliente → routes.py → services.py → models/ → Base de Datos
                                        ↓
Cliente ← routes.py ← services.py ← models/ ← Datos
```

### Petición POST (Creación)

```
Cliente (JSON) → routes.py (validación básica)
                     ↓
               services.py (validación de negocio)
                     ↓
               models/ (crear entidad)
                     ↓
               Base de Datos (INSERT)
                     ↓
Cliente ← routes.py ← services.py ← Entidad creada
```

---

## 🚨 Manejo de Errores

### Jerarquía de Excepciones

```
AppException (Base)
├── ValidationError (400)
├── NotFoundError (404)
├── ConflictError (409)
├── UnauthorizedError (401)
├── ForbiddenError (403)
├── BusinessLogicError (422)
└── DatabaseError (500)
```

### Flujo de Manejo

```python
# En services.py - Se lanza la excepción
def get_by_id(color_id: int) -> dict:
    color = Color.query.get(color_id)
    if not color:
        raise NotFoundError(f"Color con ID {color_id} no encontrado")
    return color.to_dict()


# En exceptions.py - Se captura globalmente
@app.errorhandler(AppException)
def handle_app_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
```

---

## 📦 Organización de Módulos

### Estructura de un Módulo Completo

```
app/
├── catalogs/
│   └── colors/
│       ├── __init__.py      # Blueprint
│       ├── routes.py        # Endpoints
│       ├── services.py      # Lógica de negocio
│       └── schemas.py       # Validación (opcional)
```

### Registro de Blueprints

```python
# app/__init__.py

def create_app():
    app = Flask(__name__)

    # Registrar blueprints
    from app.catalogs.colors import colors_bp
    app.register_blueprint(colors_bp, url_prefix='/api/v1/colors')

    return app
```

---

## 🔌 Extensiones y Dependencias

### Extensiones Actuales

| Extensión        | Propósito              |
|------------------|------------------------|
| Flask-SQLAlchemy | ORM para base de datos |
| Flask-Migrate    | Migraciones de BD      |

### Extensiones Recomendadas (Futuro)

| Extensión          | Propósito                     |
|--------------------|-------------------------------|
| Flask-Marshmallow  | Serialización/Validación      |
| Flask-JWT-Extended | Autenticación JWT             |
| Flask-CORS         | Cross-Origin Resource Sharing |

---

## 📁 Estructura de Archivos

```
backend-furniture-store/
│
├── app/                              # Aplicación principal
│   ├── __init__.py                   # Application Factory
│   ├── extensions.py                 # Extensiones Flask
│   ├── exceptions.py                 # Excepciones personalizadas
│   │
│   ├── catalogs/                     # Módulo de catálogos
│   │   └── colors/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── services.py
│   │
│   ├── models/                       # Modelos de datos
│   │   └── color.py
│   │
│   └── utils/                        # Utilidades comunes
│       ├── __init__.py
│       └── responses.py
│
├── docs/                             # Documentación
│   ├── ARCHITECTURE.md
│   └── CODING_CONVENTIONS.md
│
├── tests/                            # Tests (futuro)
│   └── ...
│
├── config.py                         # Configuración
├── run.py                            # Punto de entrada
├── requirements.txt
└── README.md
```

---

## ✅ Principios de Diseño

1. **Separación de Responsabilidades** - Cada capa tiene una única responsabilidad
2. **Bajo Acoplamiento** - Las capas se comunican a través de interfaces bien definidas
3. **Alta Cohesión** - Código relacionado se agrupa en el mismo módulo
4. **DRY (Don't Repeat Yourself)** - Código reutilizable en `utils/`
5. **Fail Fast** - Validar temprano, fallar con mensajes claros

