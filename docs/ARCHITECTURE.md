# 🏗️ Arquitectura Base

Este documento describe la arquitectura base del proyecto **Backend Furniture Store**.

---

## 📐 Visión General

El proyecto implementa una **arquitectura MVC en capas** (Model-View-Controller) siguiendo los principios de separación de
responsabilidades y bajo acoplamiento. Utiliza **Jinja2** como motor de templates para renderizar las vistas HTML.

```
┌─────────────────────────────────────────────────────────────────┐
│                      NAVEGADOR WEB                              │
│                   (Usuario / Cliente)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 APLICACIÓN WEB (Flask + Jinja2)                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Colors    │  │  Wood Types │  │  Furniture  │   ...        │
│  │   Module    │  │   Module    │  │   Module    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│                    CAPA DE VISTAS                               │
│              (Templates Jinja2 / HTML)                          │
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

### 1. Capa de Presentación (routes.py + forms.py + templates/)

**Responsabilidad:** Manejar las peticiones HTTP, validar formularios con WTForms y renderizar vistas HTML con Jinja2.

```python
# app/catalogs/colors/routes.py

@colors_bp.route('/create', methods=['GET', 'POST'])
def create_color():
    """Muestra el formulario y crea un nuevo color."""
    form = ColorForm()

    if form.validate_on_submit():
        data = {'name': form.name.data}
        try:
            ColorService.create(data)
            flash('Color creado exitosamente', 'success')
            return redirect(url_for('colors.create_color'))
        except ConflictError as e:
            flash(e.message, 'error')

    return render_template('colors/create.html', form=form)
```

**Características:**

- Define las rutas y renderiza templates Jinja2
- Usa `FlaskForm` para validación de formularios
- Protección CSRF automática con `form.hidden_tag()`
- Delega la lógica de negocio a la capa de servicios
- Usa `flash()` para mensajes de retroalimentación al usuario

---

### 2. Capa de Servicios (services.py)

**Responsabilidad:** Contener la lógica de negocio y orquestar operaciones.

```python
# app/catalogs/colors/services.py

class ColorService:
    @staticmethod
    def create(data: dict) -> dict:
        """Crea un nuevo color con validaciones de negocio."""
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
Navegador → routes.py → services.py → models/ → Base de Datos
                                          ↓
Navegador ← template.html ← routes.py ← services.py ← models/ ← Datos
```

### Petición POST (Creación via formulario)

```
Navegador (Form) → routes.py (recibe request.form)
                       ↓
                 services.py (validación de negocio)
                       ↓
                 models/ (crear entidad)
                       ↓
                 Base de Datos (INSERT)
                       ↓
                 routes.py → flash() + redirect
                       ↓
Navegador ← Redirección a la vista (patrón PRG)
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
def create(data: dict) -> dict:
    name = data.get('name')
    if not name or not name.strip():
        raise ValidationError('El nombre del color es requerido')
    # ...


# En routes.py - Se captura en la ruta con try/except
@colors_bp.route('/create', methods=['GET', 'POST'])
def create_color():
    form = ColorForm()
    if form.validate_on_submit():
        data = {'name': form.name.data}
        try:
            ColorService.create(data)
            flash('Color creado exitosamente', 'success')
            return redirect(url_for('colors.create_color'))
        except ConflictError as e:
            flash(e.message, 'error')
    return render_template('colors/create.html', form=form)


# En exceptions.py - Se mantiene el handler global para errores no capturados
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
│       ├── routes.py        # Rutas y controladores
│       ├── services.py      # Lógica de negocio
│       └── forms.py         # Formularios con WTForms
│
├── templates/
│   ├── base.html            # Template base (layout)
│   └── colors/
│       └── create.html       # Formulario de creación
```

### Registro de Blueprints

```python
# app/__init__.py

def create_app():
    app = Flask(__name__)

    # Registrar blueprints
    from app.catalogs.colors import colors_bp
    app.register_blueprint(colors_bp, url_prefix='/colors')

    return app
```

---

## 🔌 Extensiones y Dependencias

### Extensiones Actuales

| Extensión        | Propósito                                   |
|------------------|---------------------------------------------|
| Flask-SQLAlchemy | ORM para base de datos                      |
| Flask-Migrate    | Migraciones de BD                           |
| Flask-WTF        | Formularios con validación y protección CSRF |
| Jinja2           | Motor de templates (incluido en Flask)       |

### Extensiones Recomendadas (Futuro)

| Extensión       | Propósito                             |
|-----------------|----------------------------------------|
| Flask-Login     | Autenticación y manejo de sesiones     |
| Bootstrap/CSS   | Estilos para los templates             |

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
│   │       ├── services.py
│   │       └── forms.py
│   │
│   ├── models/                       # Modelos de datos
│   │   └── color.py
│   │
│   └── templates/                    # Templates Jinja2
│       ├── base.html                 # Template base (layout)
│       └── colors/
│           └── create.html           # Formulario de creación
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

