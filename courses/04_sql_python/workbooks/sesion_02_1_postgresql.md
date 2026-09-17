# 📓 WORKBOOK - SESIÓN 2.1
## PostgreSQL y Python con psycopg

**Curso:** Bases de Datos y SQL con Python | BSG Institute
**Fecha:** 31/08/2026
**Duración:** 2 horas (Sesión 3 de 14)

---

## 📌 ÍNDICE

1. [PostgreSQL en Docker](#1-postgresql-en-docker)
2. [Conexión desde Python](#2-conexión-desde-python)
3. [Migración de SQLite a PostgreSQL](#3-migración-de-sqlite-a-postgresql)
4. [COPY y STDIN/STDOUT](#4-copy-y-stdinst stdout)
5. [NUMERIC vs FLOAT para Dinero](#5-numeric-vs-float-para-dinero)
6. [Tipos de Datos para Porcentajes](#6-tipos-de-datos-para-porcentajes)
7. [Resumen](#7-resumen)

---

## 1. POSTGRESQL EN DOCKER

### 📋 Archivo `docker-compose.yml`

```yaml
services:
  postgres:
    image: postgres:16
    container_name: curso_postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8"
    ports:
      - "${PGPORT:-5432}:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10
    restart: unless-stopped

volumes:
  pgdata:
```

### 📋 Archivo `.env`

```env
POSTGRES_USER=datacourse
POSTGRES_PASSWORD=datacourse123
POSTGRES_DB=dataengineering
PGPORT=5432
```

### 🐳 Comandos Útiles

| Acción | Comando |
|--------|---------|
| **Levantar** | `docker compose up -d` |
| **Estado** | `docker compose ps` |
| **Logs** | `docker compose logs -f` |
| **Detener** | `docker compose down` |
| **Borrar todo** | `docker compose down -v` |

---

## 2. CONEXIÓN DESDE PYTHON

```python
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Conectar a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=os.getenv("PGPORT", "5432"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()

# Verificar conexión
cursor.execute("SELECT version()")
version = cursor.fetchone()[0]
print(f"✅ Conectado a: {version[:50]}...")

# Cerrar
cursor.close()
conn.close()
```

### 📊 Comparativa: SQLite vs PostgreSQL

| Característica | SQLite | PostgreSQL |
|----------------|--------|------------|
| **Arquitectura** | Embebido | Cliente-Servidor |
| **Configuración** | Cero | Requiere |
| **Concurrencia** | Una escritura a la vez | Múltiples escrituras |
| **Funciones avanzadas** | Limitadas | CTE, Window Functions, JSONB |
| **Python** | `sqlite3` (built-in) | `psycopg2` (instalar) |
| **Marcador de posición** | `?` | `%s` |

---

## 3. MIGRACIÓN DE SQLITE A POSTGRESQL

```python
import psycopg2
import sqlite3
import os
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

# ============================================
# 1. CONEXIÓN A SQLITE (origen)
# ============================================
conn_sqlite = sqlite3.connect("pagos.db")
cursor_sqlite = conn_sqlite.cursor()

# ============================================
# 2. CONEXIÓN A POSTGRESQL (destino)
# ============================================
conn_pg = psycopg2.connect(
    host="localhost",
    port=os.getenv("PGPORT", "5432"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cursor_pg = conn_pg.cursor()

# ============================================
# 3. CREAR TABLA EN POSTGRESQL
# ============================================
cursor_pg.execute("""
    DROP TABLE IF EXISTS movimientos CASCADE;
    CREATE TABLE movimientos (
        id SERIAL PRIMARY KEY,
        comercio TEXT,
        ciudad_comercio TEXT,
        categoria_comercio TEXT,
        monto NUMERIC(10,2),
        fecha_hora TIMESTAMP
    );
""")
conn_pg.commit()

# ============================================
# 4. EXTRAER DATOS DE SQLITE
# ============================================
cursor_sqlite.execute("""
    SELECT comercio, ciudad_comercio, categoria_comercio, monto, fecha_hora
    FROM movimientos
""")

# ============================================
# 5. CARGAR DATOS A POSTGRESQL CON COPY
# ============================================
buffer = StringIO()

for row in cursor_sqlite.fetchall():
    comercio = row[0] or ''
    ciudad = row[1] or ''
    categoria = row[2] or ''
    monto = str(row[3]) if row[3] is not None else ''
    fecha = str(row[4]) if row[4] is not None else ''
    
    buffer.write(f"{comercio}\t{ciudad}\t{categoria}\t{monto}\t{fecha}\n")

buffer.seek(0)

cursor_pg.copy_from(
    buffer,
    "movimientos",
    sep="\t",
    null="",
    columns=("comercio", "ciudad_comercio", "categoria_comercio", "monto", "fecha_hora")
)

conn_pg.commit()

# ============================================
# 6. VERIFICAR MIGRACIÓN
# ============================================
cursor_pg.execute("SELECT COUNT(*) FROM movimientos")
total = cursor_pg.fetchone()[0]
print(f"✅ Migración completada: {total} registros")

# ============================================
# 7. CERRAR CONEXIONES
# ============================================
cursor_sqlite.close()
conn_sqlite.close()
cursor_pg.close()
conn_pg.close()
```

---

## 4. COPY Y STDIN/STDOUT

> *"COPY es la forma más eficiente de mover grandes volúmenes de datos hacia o desde PostgreSQL."*

### 📊 Comparativa: INSERT vs COPY

| Método | Velocidad | Cuándo usar |
|--------|-----------|-------------|
| **INSERT** | 🟡 Lento | Pocos registros (< 1000) |
| **executemany()** | 🟡 Medio | Cientos de registros |
| **COPY** | ✅✅✅ **Muy rápido** | Miles o millones de registros |

### 🖥️ STDIN, STDOUT, STDERR

| Flujo | Sigla | Descripción |
|-------|-------|-------------|
| **STDIN** | 0 | Entrada estándar |
| **STDOUT** | 1 | Salida estándar |
| **STDERR** | 2 | Error estándar |

### 💻 Ejemplo COPY desde Python

```python
from io import StringIO

buffer = StringIO()
buffer.write("comercio,ciudad,monto\n")
buffer.write("Electrónicos,Monterrey,15000\n")
buffer.write("Restaurante,Guadalajara,250\n")
buffer.seek(0)

cursor.copy_from(
    buffer,
    "movimientos",
    sep=",",
    null="",
    columns=("comercio", "ciudad", "monto")
)
```

---

## 5. NUMERIC VS FLOAT PARA DINERO

> *"Siempre usa campos numéricos (NUMERIC/DECIMAL) si usas cantidades como dinero. FLOAT puede darte errores de redondeo."*

### 💻 Demostración del Profesor

```sql
SELECT SUM(v::float8)::text  AS suma_flotante,
       SUM(v::numeric)::text AS suma_decimal
FROM (VALUES (0.01),(0.01),(0.01),(0.01),(0.01),(0.01),(0.01),(0.01),(0.01),(0.01)) AS t(v);
```

**Resultado:**

| suma_flotante | suma_decimal |
|---------------|--------------|
| 0.0999999999999999 | 0.10 |

### 📊 Comparativa

| Aspecto | NUMERIC | FLOAT / REAL |
|---------|---------|--------------|
| **Precisión** | ✅ Exacta | ❌ Aproximada |
| **Redondeo** | ✅ Controlado | ❌ Puede fallar |
| **Uso** | Dinero, cantidades exactas | Científico, mediciones |

### 📝 Regla de Oro

> *"Si es dinero, es NUMERIC. No importa que sea más lento. La precisión es más importante que la velocidad cuando se trata de dinero."*

---

## 6. TIPOS DE DATOS PARA PORCENTAJES

| Escenario | Recomendación |
|-----------|---------------|
| **Porcentaje de avance** (0-100%) | `NUMERIC(5,2)` |
| **Tasa de interés** (ej: 0.0525) | `NUMERIC(5,4)` |
| **Probabilidad** (0-1) | `NUMERIC(4,3)` |
| **IVA (16%)** sin decimales | `SMALLINT` (16) |

### 💻 Ejemplo

```sql
CREATE TABLE proyectos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    avance NUMERIC(5,2) CHECK (avance >= 0 AND avance <= 100)
);

INSERT INTO proyectos (nombre, avance) VALUES ('Migración BD', 75.50);
```

---

## 7. RESUMEN

### 📌 Lecciones Aprendidas

1. **PostgreSQL en Docker** se levanta con `docker compose up -d`.
2. **psycopg2** es el conector de Python para PostgreSQL (usa `%s` en lugar de `?`).
3. **COPY** es la forma más rápida de migrar datos.
4. **NUMERIC** es obligatorio para dinero; **FLOAT** introduce errores de redondeo.
5. **NUMERIC(5,2)** es ideal para porcentajes.

### 🎯 Frase para Recordar
> *"El dinero no se redondea por sí solo. Si usas FLOAT, el sistema operativo o el procesador pueden introducir errores de redondeo que en finanzas son inaceptables. NUMERIC te da control total sobre la precisión."*

### 🎒 Tarea

- Practicar consultas parametrizadas con psycopg2
- Migrar datos con COPY
- Revisar tipos de datos para dinero y porcentajes

---

**¿El profesor mencionó alguna optimización adicional para la migración?** 🚀📓