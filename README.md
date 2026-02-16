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

- `.env.template` para referencia. Configurar las variables necesarias.
- No eliminar el archivo `.env.template`, solo copiar su estructura para crear `.env`.
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
backend-muebleria/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── catalogs/
│   ├── furnitures/
│   ├── .../
│   ├── models/
│
├── venv/
├── requirements.txt
├── .env
├── run.py
└── README.md
```

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
