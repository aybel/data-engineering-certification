# 📓 WORKBOOK - SESIÓN 1.1
## Fundamentos y Modelado de Datos - SQLite

**Curso:** Bases de Datos y SQL con Python | BSG Institute
**Fecha:** 11/08/2026
**Duración:** 2 horas (Sesión 1 de 14)

---

## 📌 ÍNDICE

1. [Panorama General del Curso](#1-panorama-general-del-curso)
2. [La Ficha de Seis Puntos](#2-la-ficha-de-seis-puntos)
3. [Caso de Estudio: Procesadora de Pagos](#3-caso-de-estudio-procesadora-de-pagos)
4. [SQLite: El Motor Embebido](#4-sqlite-el-motor-embebido)
5. [Código en Clase](#5-código-en-clase)
6. [Preparación del Entorno](#6-preparación-del-entorno)
7. [Ficha de SQLite](#7-ficha-de-sqlite)
8. [Resumen de la Sesión](#8-resumen-de-la-sesión)

---

## 1. PANORAMA GENERAL DEL CURSO

### 🎯 Objetivo General

Al finalizar el curso, el participante será capaz de **modelar, implementar y consultar soluciones de datos** sobre cuatro familias de bases de datos utilizando Python, y de **sustentar ante un comité técnico** la selección del motor adecuado para un requerimiento determinado.

### 📊 Las Cuatro Familias de Bases de Datos

| Familia | Motor | Optimiza | Cede |
|---------|-------|----------|------|
| **Relacional** | PostgreSQL | Integridad, relaciones y consulta expresiva | Flexibilidad del esquema |
| **Documental** | MongoDB | Esquema variable y lectura de agregados completos | Consistencia entre colecciones |
| **Clave-Valor** | Redis | Latencia muy baja en acceso por clave | Capacidad de consulta |
| **Analítico Columnar** | BigQuery | Agregación sobre volumen alto | Escritura por registro individual |

> 💡 **Clave:** La columna **CEDE** es la que sostiene la decisión de arquitectura. Elegir un motor implica aceptar lo que ese motor entrega a cambio.

### ❓ Pregunta del Profesor

> *"¿Por qué existen tantas bases de datos? ¿Por qué tantas familias?"*

**Respuesta:** No hay una base de datos que sea la mejor para todo. Cada una está diseñada para resolver un **tipo específico de problema**:

| Tipo de Dato | Motor Ideal |
|--------------|-------------|
| Relacional, con relaciones | PostgreSQL, MySQL |
| Documentos, no estructurado | MongoDB |
| Clave-Valor, alta velocidad | Redis |
| Analítico, grandes volúmenes | BigQuery |

---

## 2. LA FICHA DE SEIS PUNTOS

> *"Cada motor del curso se documenta con esta misma estructura. Al cierre, el conjunto de fichas constituye la matriz de decisión que se evalúa en el proyecto final."*

### 📋 Estructura de la Ficha

| # | Punto | Pregunta Clave |
|---|-------|----------------|
| **1** | **Modelo de datos que asume** | ¿Qué estructura de datos espera el motor? |
| **2** | **Operaciones en las que resulta eficiente** | ¿Qué sabe hacer bien? |
| **3** | **Garantías de consistencia que ofrece** | ¿Qué tan confiable es con los datos? |
| **4** | **Relación entre costo de escritura y costo de lectura** | ¿Es más caro escribir o leer? |
| **5** | **Interfaz desde Python** | ¿Cómo nos conectamos desde Python? |
| **6** | **Escenario en el que conviene y en el que no** | ¿Cuándo usar este motor y cuándo evitarlo? |

### 🗂️ La Matriz de Decisión

| Punto | SQLite | PostgreSQL | MongoDB | Redis | BigQuery |
|-------|--------|------------|---------|-------|----------|
| **1** | | | | | |
| **2** | | | | | |
| **3** | | | | | |
| **4** | | | | | |
| **5** | | | | | |
| **6** | | | | | |

*(Se irá llenando a lo largo del curso)*

---

## 3. CASO DE ESTUDIO: PROCESADORA DE PAGOS

> *"Todas las sesiones del curso trabajan sobre el mismo dominio. La continuidad permite que la comparación entre motores sea directa: la misma pregunta de negocio se resuelve cuatro veces, con cuatro tecnologías."*

### 🏗️ Entidades del Sistema

- **🏪 COMERCIOS** → Negocios que aceptan pagos con tarjeta
- **📟 TERMINALES** → Dispositivos físicos donde se cobra
- **👤 CLIENTES** → Personas que realizan pagos
- **💳 TARJETAS** → Tarjetas de crédito/débito
- **💰 TRANSACCIONES** → Cada operación de pago
- **🔄 CONTRACARGOS** → Disputas / reclamos por cargos no reconocidos

### ❓ Preguntas de Negocio

| # | Pregunta | Motor Ideal | ¿Por qué? |
|---|----------|-------------|-----------|
| 1 | ¿Cuánto vendió cada comercio este mes? | **PostgreSQL** | Joins y agregaciones |
| 2 | ¿Esta tarjeta se sale de su patrón habitual? | **MongoDB** | Logs de comportamiento |
| 3 | ¿Cuántos intentos lleva esta tarjeta en un minuto? | **Redis** | Alta velocidad, clave-valor |
| 4 | ¿Cómo evolucionó el ticket promedio en dos años? | **BigQuery** | Gran volumen analítico |

> 💡 **En palabras simples:** "Cada pregunta de negocio tiene un motor que la resuelve mejor. La clave es saber cuándo usar cada uno."

---

## 4. SQLITE: EL MOTOR EMBEBIDO

> *"SQLite es el primer motor que vamos a conocer. Es el más simple, el que no necesita servidor, el que cabe en un archivo."*

### 📌 ¿Qué es SQLite?

| Característica | Descripción |
|----------------|-------------|
| **Tipo** | Base de datos relacional (SQL) |
| **Arquitectura** | Sin servidor (embedded) |
| **Almacenamiento** | Un solo archivo `.db` en disco |
| **Lenguaje** | SQL estándar |
| **ACID** | ✅ Sí, completamente ACID |
| **Python** | Viene incluido en la biblioteca estándar (`sqlite3`) |

### ✅ Ventajas de SQLite

- **Portable:** El archivo .db se mueve a cualquier sistema
- **Rápido:** Para lecturas y operaciones pequeñas
- **Confiabilidad:** ACID garantiza que los datos no se corrompan
- **Sin dependencias:** No requiere instalar un servidor
- **Ideal para:** Aplicaciones móviles, prototipos, pruebas unitarias

### ❌ Limitaciones de SQLite

- **Escritura concurrente:** Solo permite UNA escritura a la vez
- **Escalabilidad:** No está diseñado para grandes volúmenes
- **Funciones avanzadas:** No tiene todo lo que PostgreSQL ofrece
- **Multi-usuario:** No es para aplicaciones con muchos usuarios concurrentes

### 💡 En Palabras Simples

> *"SQLite es como una libreta de apuntes. La usas para ti, la guardas en tu bolsillo, y no necesitas nada más. Pero si quieres que otros escriban al mismo tiempo, necesitas algo más grande."*

---

## 5. CÓDIGO EN CLASE

### 🔌 DB-API 2.0: El Estándar

> *"DB-API 2.0 es el estándar que permite a Python hablar con cualquier base de datos de la misma manera."*

**Elementos obligatorios de DB-API 2.0:**

| Elemento | En `sqlite3` |
|----------|--------------|
| `connect()` | `sqlite3.connect('archivo.db')` |
| `Connection` | `conn = sqlite3.connect(...)` |
| `Cursor` | `cursor = conn.cursor()` |
| `execute()` | `cursor.execute("SELECT ...")` |
| `fetchone()` | `row = cursor.fetchone()` |
| `fetchall()` | `rows = cursor.fetchall()` |
| `commit()` | `conn.commit()` |
| `rollback()` | `conn.rollback()` |
| `close()` | `conn.close()` |

### 💻 Crear Tabla e Insertar Registro

```python
import sqlite3

# 1. CONECTAR (crea pagos.db si no existe)
conexion = sqlite3.connect("pagos.db")
cursor = conexion.cursor()

# 2. CREAR TABLA
cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comercio_id INTEGER,
        tarjeta_id INTEGER,
        monto REAL,
        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

# 3. INSERTAR UN REGISTRO
cursor.execute("""
    INSERT INTO movimientos (comercio_id, tarjeta_id, monto)
    VALUES (1, 1001, 150.50)
""")

# 4. CONFIRMAR LA INSERCIÓN (¡IMPORTANTE!)
conexion.commit()

# 5. CONTAR REGISTROS
cursor.execute("SELECT COUNT(*) FROM movimientos")
total = cursor.fetchone()[0]
print(f"Transacciones en la base: {total}")

# 6. CERRAR CONEXIÓN
conexion.close()
```

**Resultado:**
```
Transacciones en la base: 1
```

> ⚠️ **Apunte clave:** El `commit()` es lo que guarda los cambios en el archivo. Sin `commit()`, el registro se pierde al cerrar la conexión.

---

## 6. PREPARACIÓN DEL ENTORNO

### ✅ Lo que ya tienes en tu Data Lab

| Componente | Estado |
|------------|--------|
| **Python 3.11** | ✅ |
| **pip** | ✅ |
| **Docker** | ✅ |
| **JupyterLab** | ✅ |
| **pandas** | ✅ |
| **polars** | ✅ |
| **sqlite3** | ✅ (viene con Python) |

### 🚀 Pasos para Organizar el Repositorio

```bash
# 1. Crear la carpeta del curso
cd ~/data-engineering-certification
mkdir -p courses/04_sql_python/{notebooks,scripts,data/raw}

# 2. Mover archivos del curso
cp ~/Downloads/c1_s1_b1_instalacion.md courses/04_sql_python/
cp ~/Downloads/c1_s1_b2_generar_datos.py courses/04_sql_python/scripts/
cp ~/Downloads/pagos_plano.csv courses/04_sql_python/data/raw/
cp ~/Downloads/pagos.db courses/04_sql_python/
```

---

## 7. FICHA DE SQLITE

| # | Punto | SQLite |
|---|-------|--------|
| **1** | **Modelo de datos que asume** | Relacional (tablas con columnas y filas) |
| **2** | **Operaciones eficientes** | Lecturas, consultas simples, CRUD básico |
| **3** | **Garantías de consistencia** | ACID completo (Atomicidad, Consistencia, Aislamiento, Durabilidad) |
| **4** | **Costo escritura vs lectura** | Escritura costosa (bloquea toda la BD); lectura barata |
| **5** | **Interfaz desde Python** | `sqlite3` (biblioteca estándar) + `pandas.read_sql_query()` |
| **6** | **Conviene / No conviene** | ✅ Prototipos, móvil, pruebas unitarias<br>❌ Alta concurrencia, grandes volúmenes, producción pesada |

---

## 8. RESUMEN DE LA SESIÓN

### 📌 Lecciones Aprendidas

1. **Existen diferentes familias de bases de datos** porque cada una resuelve un problema específico.
2. **La ficha de 6 puntos** es el método transversal para evaluar cada motor.
3. **SQLite es el motor más simple** para empezar: sin servidor, sin configuración, en un archivo.
4. **La DB-API 2.0** es el estándar que uniforma la conexión desde Python.
5. **El caso de estudio (procesadora de pagos)** será el hilo conductor de todo el curso.

### 🗂️ Archivos Generados en la Sesión

```
📁 courses/04_sql_python/
├── 📄 pagos.db                  # Base de datos SQLite
├── 📄 README.md                 # Documentación del curso
├── 📁 data/raw/
│   └── 📄 pagos_plano.csv       # Extracto operativo plano
└── 📁 scripts/
    ├── 📄 c1_s1_b2_generar_datos.py
    └── 📄 c1_s1_b3_primer_contacto.py
```

### 🎯 Preparado para la Próxima Sesión (1.2)

- ✅ Entorno de trabajo listo
- ✅ Datos cargados en SQLite
- ✅ Conexión verificada desde Python
- ✅ Ficha de SQLite completada

---

**Nota final:** *"SQLite es el cuaderno de notas de las bases de datos. No es para producción pesada, pero es perfecto para aprender, para probar ideas, y para proyectos pequeños. Cuando necesites más, saltas a PostgreSQL. Pero sin SQLite, no entenderías los fundamentos."*

---