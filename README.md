# Sistema de Gestión de Mueblería – Backend

Backend desarrollado en **Flask** para la gestión del proceso productivo de una mueblería, permitiendo administrar:

* Inventario de materia prima (madera e insumos)
* Inventario de productos terminados (mesas, sillas, closets, etc.)
* Catálogos (tipos de madera, colores, tipos de muebles)
* Procesos de producción
* Control de inventario y trazabilidad

Este sistema forma parte de un proyecto académico orientado a la industria de transformación, donde se controla el flujo
desde la materia prima hasta el producto terminado.

---

## 🛠️ Tecnologías Utilizadas

* Python 3.10.11
* Flask
* Flask SQLAlchemy
* Base de datos relacional (MySQL)
* pip
* Virtual Environment (venv)

---

## 🐍 Requisitos

Este proyecto requiere:

* **Python 3.10.11**
* pip

Verificar versión instalada:

```bash
python --version
```

Debe mostrar:

```bash
Python 3.10.11
```

---

## ⚙️ Configuración del Entorno

### 1️⃣ Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd backend-muebleria
```

---

### 2️⃣ Crear entorno virtual

```bash
python -m venv venv
```

---

### 3️⃣ Activar entorno virtual

### En Windows:

```bash
venv\Scripts\activate
```

### En Mac/Linux:

```bash
source venv/bin/activate
```

Si se activó correctamente, verás `(venv)` al inicio de la consola.

---

### 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ⚙️ Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

- `.env-template` para referencia. Configurar las variables necesarias.
- No eliminar el archivo `.env-template`, solo copiar su estructura para crear `.env`.
- No subir el archivo `.env` al repositorio, ya que contiene información sensible.

---

## ▶️ Ejecutar el Proyecto

Si usas Flask CLI:

```bash
flask run
```

O directamente:

```bash
python run.py
```

El servidor iniciará en:

```
http://127.0.0.1:5000
```

---

## 🧪 Ejecutar Pruebas (Opcional)

```bash
pytest
```

---

## 📂 Estructura del Proyecto

```
backend-furniture-store/
│
├── app/                          # Paquete principal de la aplicación
│   ├── __init__.py               # Factory de la aplicación Flask (create_app)
│   ├── extensions.py             # Extensiones de Flask (SQLAlchemy, Migrate)
│   ├── exceptions.py             # Excepciones personalizadas y manejo de errores
│   │
│   ├── catalogs/                 # Módulo de catálogos
│   │   └── colors/               # Submódulo de colores
│   │       ├── __init__.py
│   │       ├── routes.py         # Endpoints/Rutas de la API
│   │       └── services.py       # Lógica de negocio
│   │
│   ├── models/                   # Capa de modelos (entidades de BD)
│   │   └── color.py              # Modelo de Color
│   │
│   └── utils/                    # Utilidades comunes
│       ├── __init__.py
│       └── responses.py          # Respuestas HTTP estandarizadas
│
├── docs/                         # Documentación del proyecto
│   ├── ARCHITECTURE.md           # Documentación de arquitectura
│   └── CODING_CONVENTIONS.md     # Convenciones de código
│
├── config.py                     # Configuración del proyecto
├── run.py                        # Punto de entrada de la aplicación
├── requirements.txt              # Dependencias del proyecto
├── .env                          # Variables de entorno (no versionar)
├── .env-template                 # Plantilla de variables de entorno
└── README.md
```

---

## 🏗️ Arquitectura en Capas

El proyecto está diseñado siguiendo una **arquitectura en capas** para separar responsabilidades y facilitar el
mantenimiento:

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│                      (routes.py)                            │
│         Endpoints REST API / Controladores                  │
├─────────────────────────────────────────────────────────────┤
│                  CAPA DE LÓGICA DE NEGOCIO                  │
│                      (services.py)                          │
│     Reglas de negocio / Validaciones / Procesamiento        │
├─────────────────────────────────────────────────────────────┤
│                    CAPA DE DATOS/MODELOS                    │
│                       (models/)                             │
│          Entidades / ORM SQLAlchemy / Base de Datos         │
└─────────────────────────────────────────────────────────────┘
```

### 📁 Descripción de Capas

| Capa              | Archivos                     | Responsabilidad                                                                        |
|-------------------|------------------------------|----------------------------------------------------------------------------------------|
| **Presentación**  | `routes.py`                  | Define los endpoints de la API REST, recibe peticiones HTTP y devuelve respuestas JSON |
| **Servicios**     | `services.py`                | Contiene la lógica de negocio, validaciones y orquestación de operaciones              |
| **Modelos**       | `models/*.py`                | Define las entidades y su mapeo a tablas de base de datos usando SQLAlchemy ORM        |
| **Configuración** | `config.py`, `extensions.py` | Configuración del entorno, conexión a BD y extensiones de Flask                        |

### 📦 Organización por Módulos

El proyecto organiza las funcionalidades en **módulos de dominio** dentro de `app/`:

```
app/
├── catalogs/           # Catálogos del sistema
│   ├── colors/         # Gestión de colores
│   ├── wood_types/     # Tipos de madera (futuro)
│   └── furniture_types/# Tipos de muebles (futuro)
│
├── inventory/          # Control de inventario (futuro)
├── production/         # Procesos de producción (futuro)
└── models/             # Todos los modelos de la aplicación
```

### 🔄 Flujo de una Petición

```
Cliente HTTP
     │
     ▼
┌─────────────┐
│  routes.py  │  ← Recibe la petición, valida parámetros
└─────────────┘
     │
     ▼
┌─────────────┐
│ services.py │  ← Ejecuta lógica de negocio
└─────────────┘
     │
     ▼
┌─────────────┐
│  models/    │  ← Interactúa con la base de datos
└─────────────┘
     │
     ▼
  Base de Datos (MySQL)
```

---

## 📚 Documentación Adicional

| Documento                                               | Descripción                                         |
|---------------------------------------------------------|-----------------------------------------------------|
| [📐 Arquitectura](docs/ARCHITECTURE.md)                 | Documentación detallada de la arquitectura en capas |
| [📋 Convenciones de Código](docs/CODING_CONVENTIONS.md) | Estándares y convenciones de desarrollo             |

---

## 📊 Funcionalidades Principales

* Gestión de tipos de madera (Pino, Cedro, Encino)
* Gestión de colores (Natural, Blanco, Negro, etc.)
* Registro de muebles (Mesas, Sillas, Closets, etc.)
* Control de inventario de materia prima
* Registro de producción
* Control de productos terminados
* Auditoría de operaciones

---

## 🚫 Importante

- El archivo `.gitignore` se debe de editar con precaución.
- Actualizar el README para documentar el proyecto.

---

## 👤 Autor

Lattice Systems

Ingeniería en Desarrollo y Gestión de Software
Backend Developer – Sistema de Gestión de Mueblería
