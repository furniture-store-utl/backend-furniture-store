# Guía Oficial de Migraciones

## Proyecto Backend con Flask + SQLAlchemy + Flask-Migrate

---

# Objetivo

Establecer un estándar de trabajo para el manejo de migraciones de base de datos en el proyecto, asegurando:

* Consistencia del esquema
* Trabajo en equipo sin conflictos
* Historial limpio de cambios
* Prevención de errores en producción

---

# Tecnologías Utilizadas

* Flask
* SQLAlchemy
* Flask-Migrate
* Alembic (internamente)

---

# Configuración Inicial (Solo una vez por proyecto)

```bash
flask db init
```

Esto crea la carpeta `migrations/`.

⚠️ Este comando solo debe ejecutarse una vez en todo el proyecto.

---

# Flujo Oficial de Trabajo en Equipo

## 1️⃣ Antes de comenzar a trabajar

Siempre ejecutar:

```bash
git pull
flask db upgrade
```

Esto asegura que tu base de datos esté sincronizada con el repositorio.

---

## 2️⃣ Cuando modificas modelos

Después de crear o modificar un modelo:

```bash
flask db migrate -m "describe change"
flask db upgrade
```

Luego hacer commit:

```bash
git add .
git commit -m "migration: describe change"
git push
```

---

# Comandos Fundamentales

| Comando                   | Descripción                      |
|---------------------------|----------------------------------|
| flask db init             | Inicializa migraciones           |
| flask db migrate -m "msg" | Genera nueva migración           |
| flask db upgrade          | Aplica migraciones pendientes    |
| flask db downgrade        | Revierte última migración        |
| flask db history          | Ver historial de versiones       |
| flask db current          | Ver versión actual aplicada      |
| flask db heads            | Ver múltiples ramas de migración |
| flask db merge -m "msg"   | Fusionar heads                   |
| flask db stamp head       | Marcar versión sin ejecutar      |

---

# Buenas Prácticas Obligatorias

## 1. Siempre hacer upgrade antes de trabajar

Nunca generar migraciones sin antes sincronizar tu base de datos.

---

## 2. No modificar manualmente archivos en migrations/versions

Solo en casos avanzados y con revisión del equipo.

---

## 3. Mensajes de migración descriptivos

❌ Incorrecto:

```
update
```

✅ Correcto:

```
add price column to products table
```

---

## 4. Una migración por cambio lógico

Evitar mezclar múltiples cambios grandes en una sola migración.

---

## 5. Las migraciones siempre se versionan

La carpeta `migrations/` debe estar incluida en el repositorio.

---

# Resolución de Conflictos

## Caso: Existen múltiples heads

Detectar:

```bash
flask db heads
```

Si aparecen múltiples resultados:

```bash
flask db merge -m "merge heads"
flask db upgrade
```

Luego hacer commit del archivo generado.

---

# Checklist para Pull Requests con Migraciones

Antes de aprobar un Pull Request que incluya migraciones, validar lo siguiente:

* [ ] La migración fue generada automáticamente mediante `flask db migrate`.
* [ ] El mensaje de migración describe claramente el cambio realizado.
* [ ] El desarrollador ejecutó `flask db upgrade` localmente sin errores.
* [ ] Se verificó que la migración funciona en una base de datos limpia.
* [ ] No se eliminan columnas o tablas sin justificación técnica documentada.
* [ ] No se modifican tipos de datos sensibles sin evaluar impacto en datos existentes.
* [ ] No contiene lógica de negocio dentro del archivo de migración.
* [ ] El archivo de migración está incluido en el commit.

---

# Flujo Completo Desde Cero

```bash
git clone repo
cd project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
```

---

# Errores Comunes

### No detecta cambios

* Verificar que el modelo esté importado
* Confirmar que esté registrado en SQLAlchemy

### Error al hacer downgrade

* Revisar dependencias entre tablas
* Verificar claves foráneas

---

# Conclusión

Siguiendo esta guía el equipo podrá:

* Trabajar en paralelo sin romper la base de datos
* Mantener un historial limpio
* Resolver conflictos de migraciones
* Evitar errores en producción

