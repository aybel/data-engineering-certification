# 📓 WORKBOOK - SESIÓN 1.2
## Normalización de Bases de Datos

**Curso:** Bases de Datos y SQL con Python | BSG Institute
**Fecha:** 20/08/2026
**Duración:** 2 horas (Sesión 2 de 14)

---

## 📌 ÍNDICE

1. [¿Qué es la Normalización?](#1-qué-es-la-normalización)
2. [Anomalías que Previene](#2-anomalías-que-previene)
3. [Primera Forma Normal (1FN)](#3-primera-forma-normal-1fn)
4. [Segunda Forma Normal (2FN)](#4-segunda-forma-normal-2fn)
5. [Tercera Forma Normal (3FN)](#5-tercera-forma-normal-3fn)
6. [Cuarta y Quinta Forma Normal (4FN y 5FN)](#6-cuarta-y-quinta-forma-normal-4fn-y-5fn)
7. [Implementación en SQLite](#7-implementación-en-sqlite)
8. [Resumen](#8-resumen)

---

## 1. ¿QUÉ ES LA NORMALIZACIÓN?

**Definición:** Proceso de organizar los datos en tablas para:
- **Eliminar redundancias** (datos duplicados)
- **Garantizar integridad** (que los datos sean consistentes)
- **Evitar anomalías** al insertar, actualizar o eliminar registros

**Analogía:** Como organizar un armario: separar por tipo de prenda, color y temporada para encontrar todo más fácil.

---

## 2. ANOMALÍAS QUE PREVIENE

| Anomalía | Ejemplo |
|----------|---------|
| **Inserción** | No puedes agregar un comercio sin una transacción |
| **Actualización** | Cambiar el nombre de un comercio en 500 registros |
| **Eliminación** | Borrar un comercio y perder todas sus transacciones |

---

## 3. PRIMERA FORMA NORMAL (1FN)

**Regla:** Cada celda contiene un solo valor atómico (no listas ni grupos repetidos).

### ❌ Ejemplo NO 1FN

| id | nombre | teléfonos |
|----|--------|-----------|
| 1 | Juan | 555-1234, 555-5678 |

### ✅ Ejemplo 1FN

| id | nombre | teléfono |
|----|--------|----------|
| 1 | Juan | 555-1234 |
| 1 | Juan | 555-5678 |

---

## 4. SEGUNDA FORMA NORMAL (2FN)

**Regla:** Ya está en 1FN y todos los atributos NO clave dependen de TODA la llave primaria (dependencia funcional completa).

### ❌ Ejemplo NO 2FN

**Tabla: `compras`**

| cliente_id | producto_id | nombre_cliente | nombre_producto | precio |
|------------|-------------|----------------|-----------------|--------|
| 1 | A1 | Juan | Laptop | 15000 |
| 1 | B2 | Juan | Mouse | 250 |

**Llave primaria:** `(cliente_id, producto_id)`

**Problema:** `nombre_cliente` depende solo de `cliente_id` (parte de la llave). `nombre_producto` depende solo de `producto_id`.

### ✅ Solución 2FN (Tres tablas)

**Tabla: `clientes`**

| id | nombre |
|----|--------|
| 1 | Juan |

**Tabla: `productos`**

| id | nombre | precio |
|----|--------|--------|
| A1 | Laptop | 15000 |
| B2 | Mouse | 250 |

**Tabla: `compras`**

| cliente_id | producto_id |
|------------|-------------|
| 1 | A1 |
| 1 | B2 |

---

## 5. TERCERA FORMA NORMAL (3FN)

**Regla:** Ya está en 2FN y no hay dependencias transitivas (un atributo no clave no depende de otro atributo no clave).

### ❌ Ejemplo NO 3FN

**Tabla: `empleados`**

| id | nombre | departamento_id | nombre_departamento |
|----|--------|-----------------|---------------------|
| 1 | Juan | 10 | Ventas |
| 2 | Ana | 20 | Marketing |

**Problema:** `nombre_departamento` depende de `departamento_id`, no directamente de `id`.

### ✅ Solución 3FN (Dos tablas)

**Tabla: `empleados`**

| id | nombre | departamento_id |
|----|--------|-----------------|
| 1 | Juan | 10 |
| 2 | Ana | 20 |

**Tabla: `departamentos`**

| id | nombre |
|----|--------|
| 10 | Ventas |
| 20 | Marketing |

---

## 6. CUARTA Y QUINTA FORMA NORMAL (4FN Y 5FN)

> *"El profesor solo mencionó 4FN y 5FN de forma teórica. En la práctica, la mayoría de los proyectos llegan hasta 3FN."*

| Forma | Regla | Problema que resuelve |
|-------|-------|----------------------|
| **4FN** | Sin dependencias multivaluadas | Atributos independientes que dependen de la misma llave |
| **5FN** | Sin dependencias de combinación | Tablas que se pueden descomponer y recomponer |

### 💡 En Palabras Simples

**4FN:** *"Si tienes dos listas independientes que dependen de una misma llave, sepáralas en tablas diferentes."*

**5FN:** *"Si tu tabla se puede dividir en varias tablas y combinarlas para recuperar la original sin perder información, entonces debes dividirla."*

---

## 7. IMPLEMENTACIÓN EN SQLITE

```python
import sqlite3

# Conectar
conexion = sqlite3.connect("pagos.db")
cursor = conexion.cursor()

# ============================================
# 1. CREAR TABLAS NORMALIZADAS
# ============================================

# Tabla de categorías
cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
""")

# Tabla de comercios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS comercios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        ciudad TEXT NOT NULL,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
""")

# Tabla de movimientos normalizada
cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_normalizado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comercio_id INTEGER NOT NULL,
        monto REAL NOT NULL,
        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (comercio_id) REFERENCES comercios(id)
    )
""")

# ============================================
# 2. POBLAR CATÁLOGOS
# ============================================

cursor.execute("""
    INSERT OR IGNORE INTO categorias (nombre)
    SELECT DISTINCT categoria_comercio
    FROM movimientos
    WHERE categoria_comercio IS NOT NULL AND categoria_comercio != ''
""")

cursor.execute("""
    INSERT OR IGNORE INTO comercios (nombre, ciudad, categoria_id)
    SELECT DISTINCT
        m.comercio,
        m.ciudad_comercio,
        c.id
    FROM movimientos m
    LEFT JOIN categorias c ON m.categoria_comercio = c.nombre
    WHERE m.comercio IS NOT NULL AND m.comercio != ''
""")

# ============================================
# 3. MIGRAR MOVIMIENTOS
# ============================================

cursor.execute("""
    INSERT INTO movimientos_normalizado (comercio_id, monto, fecha_hora)
    SELECT
        co.id,
        m.monto,
        m.fecha_hora
    FROM movimientos m
    INNER JOIN comercios co ON m.comercio = co.nombre
""")

conexion.commit()

# ============================================
# 4. VERIFICAR
# ============================================

cursor.execute("SELECT COUNT(*) FROM categorias")
print(f"Categorías: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM comercios")
print(f"Comercios: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM movimientos_normalizado")
print(f"Movimientos: {cursor.fetchone()[0]}")

# ============================================
# 5. CONSULTA NORMALIZADA
# ============================================

cursor.execute("""
    SELECT
        c.nombre AS comercio,
        COUNT(m.id) AS operaciones,
        ROUND(SUM(m.monto), 2) AS importe_total
    FROM movimientos_normalizado m
    INNER JOIN comercios c ON m.comercio_id = c.id
    GROUP BY c.id, c.nombre
    ORDER BY operaciones DESC
""")

for row in cursor.fetchall():
    print(f"  {row[0]:<22} {row[1]:>5} operaciones   ${row[2]:>12,.2f}")

conexion.close()
```

---

## 8. RESUMEN

### 📌 Lecciones Aprendidas

1. **1FN:** Valores atómicos, sin listas.
2. **2FN:** Dependencia completa de la llave primaria.
3. **3FN:** Dependencia directa de la llave primaria.
4. **4FN y 5FN:** Casos muy específicos, raramente usados en la práctica.
5. **Catálogos:** Tablas maestras (comercios, categorías).
6. **JOIN:** Unir tablas para consultas completas.

### 🎯 Frase para Recordar

> *"Normalizar es como tener un catálogo: los comercios están una sola vez, las categorías una sola vez, y las transacciones solo referencian a estos catálogos."*

---

**¿El profesor mencionó si van a ver 4FN o 5FN en sesiones posteriores?** 🚀📓