# 📓 WORKBOOK - SESIÓN 10-11
## JSONB en PostgreSQL y SQLAlchemy

**Curso:** Bases de Datos y SQL con Python | BSG Institute
**Fecha:** 15/09/2026
**Duración:** 4 horas (2 sesiones)

---

## 📌 ÍNDICE

1. [¿Qué son los Datos Semiestructurados?](#1-qué-son-los-datos-semiestructurados)
2. [JSON vs JSONB](#2-json-vs-jsonb)
3. [Operadores de Acceso](#3-operadores-de-acceso)
4. [Operadores de Búsqueda](#4-operadores-de-búsqueda)
5. [Operador de Contención](#5-operador-de-contención)
6. [Índices GIN](#6-índices-gin)
7. [SQLAlchemy ORM](#7-sqlalchemy-orm)
8. [Ejemplo con la Tabla transacciones](#8-ejemplo-con-la-tabla-transacciones)
9. [Resumen](#9-resumen)

---

## 1. ¿QUÉ SON LOS DATOS SEMIESTRUCTURADOS?

> *"Datos que no tienen un esquema rígido como las tablas relacionales, pero que sí tienen una estructura flexible basada en pares clave-valor."*

| Tipo | Estructura | Ejemplo |
|------|------------|---------|
| **Estructurado** | Tablas, columnas fijas | `movimientos(id, monto, fecha)` |
| **Semiestructurado** | JSON, XML | `{"id": 1, "monto": 100}` |
| **No estructurado** | Texto libre | Correos, fotos |

---

## 2. JSON VS JSONB

| Característica | JSON | JSONB |
|----------------|------|-------|
| **Almacenamiento** | Texto plano | Binario |
| **Velocidad de escritura** | ✅ Rápido | 🟡 Más lento |
| **Velocidad de lectura** | 🟡 Lento | ✅ Rápido |
| **Índices** | ❌ No soporta | ✅ Soporta GIN |
| **Operadores** | Limitados | ✅ Completos |

> *"Siempre usa JSONB a menos que necesites preservar el orden exacto de las claves."*

---

## 3. OPERADORES DE ACCESO

| Operador | Devuelve | Ejemplo |
|----------|----------|---------|
| `->` | JSON | `autorizacion->'captura'` |
| `->>` | Texto | `autorizacion->>'captura'` |
| `#>` | JSON en ruta | `autorizacion#>'{captura,metodo}'` |
| `#>>` | Texto en ruta | `autorizacion#>>'{captura,metodo}'` |

### 💻 Ejemplos

```sql
-- Acceder a campos anidados
SELECT autorizacion->'captura'->>'metodo' AS metodo FROM transacciones;
SELECT autorizacion->'emisor'->>'nombre' AS banco FROM transacciones;
SELECT autorizacion#>>'{dispositivo,ubicacion,lat}' AS latitud FROM transacciones;
```

---

## 4. OPERADORES DE BÚSQUEDA

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `?` | ¿Existe la clave? | `autorizacion ? 'rechazo'` |
| `?&` | ¿Existen TODAS las claves? | `autorizacion ?& array['emisor', 'riesgo']` |
| `?|` | ¿Existe ALGUNA clave? | `autorizacion ?| array['captura', 'rechazo']` |

### 💻 Ejemplos

```sql
SELECT * FROM transacciones WHERE autorizacion ? 'rechazo';
SELECT * FROM transacciones WHERE autorizacion ?& array['emisor', 'riesgo'];
SELECT * FROM transacciones WHERE autorizacion ?| array['captura', 'rechazo'];
```

---

## 5. OPERADOR DE CONTENCIÓN

**Definición:** `@>` verifica si el JSONB de la izquierda **contiene** el JSONB de la derecha.

### 💻 Ejemplo del Profesor

```sql
SELECT
    metodo_captura,
    autorizacion @> '{"rechazo":{"codigo":"LIMITE_EXEDIDO"}}'
FROM
    transacciones;
```

### 💻 Más Ejemplos

```sql
-- Transacciones rechazadas por fondos insuficientes
SELECT * FROM transacciones
WHERE autorizacion @> '{"rechazo":{"codigo":"FONDOS_INSUFICIENTES"}}';

-- Transacciones de Scotiabank
SELECT * FROM transacciones
WHERE autorizacion @> '{"emisor":{"nombre":"SCOTIABANK"}}';
```

---

## 6. ÍNDICES GIN

> *"El índice GIN es lo que hace que JSONB sea realmente poderoso. Sin índice, cada consulta tiene que leer toda la tabla."*

### 📊 Comparativa de Índices

| Tipo de índice | Soporta | Tamaño |
|----------------|---------|--------|
| **GIN completo** | `@>`, `?`, `?&`, `?|` | Grande |
| **GIN por clave** | `@>` en esa clave | Mediano |
| **GIN por ruta** | `@>` en esa ruta | Pequeño |
| **jsonb_path_ops** | Solo `@>` | Pequeño |

### 💻 Crear Índice GIN

```sql
-- Índice completo
CREATE INDEX idx_autorizacion_gin ON transacciones USING GIN (autorizacion);

-- Índice por clave
CREATE INDEX idx_autorizacion_rechazo_gin ON transacciones USING GIN ((autorizacion->'rechazo'));

-- Índice por ruta
CREATE INDEX idx_autorizacion_codigo_gin ON transacciones USING GIN ((autorizacion#>>'{rechazo,codigo}'));
```

### 💻 Medir Rendimiento

```sql
-- Sin índice
EXPLAIN ANALYZE
SELECT * FROM transacciones
WHERE autorizacion @> '{"rechazo":{"codigo":"LIMITE_EXEDIDO"}}';

-- Con índice
CREATE INDEX idx_autorizacion_gin ON transacciones USING GIN (autorizacion);
EXPLAIN ANALYZE
SELECT * FROM transacciones
WHERE autorizacion @> '{"rechazo":{"codigo":"LIMITE_EXEDIDO"}}';
```

---

## 7. SQLALCHEMY ORM

### 🧠 ¿Qué es un ORM?

> *"Un ORM (Object-Relational Mapper) es una capa de software que traduce entre el mundo de los objetos de Python y el mundo de las tablas de una base de datos relacional."*

### 📊 Analogía

| Mundo Python | ORM | Mundo Base de Datos |
|--------------|-----|---------------------|
| **Clase** | ↔️ | **Tabla** |
| **Objeto** | ↔️ | **Fila** |
| **Atributo** | ↔️ | **Columna** |

### 💻 Modelo en SQLAlchemy 2.0

```python
from sqlalchemy import create_engine, Column, String, Integer, Numeric, TIMESTAMP, CHAR
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Transaccion(Base):
    __tablename__ = 'transacciones'
    
    id_transaccion = Column(String(20), primary_key=True)
    fecha_hora = Column(TIMESTAMP, nullable=False)
    id_terminal = Column(Integer, nullable=False)
    id_tarjeta = Column(Integer, nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    moneda = Column(CHAR(3), nullable=False, default='MXN')
    estatus = Column(String(20), nullable=False)
    metodo_captura = Column(String(20), nullable=False)
    autorizacion = Column(JSONB, nullable=True)
```

---

## 8. EJEMPLO CON LA TABLA TRANSACCIONES

### 💻 Insertar con SQLAlchemy

```python
trans = Transaccion(
    id_transaccion="TXN-2024-001",
    fecha_hora=datetime(2024, 1, 15, 10, 30, 0),
    id_terminal=1,
    id_tarjeta=1001,
    monto=15000.00,
    estatus="APROBADA",
    metodo_captura="CHIP",
    autorizacion={
        "emisor": {"pais": "MX", "nombre": "SCOTIABANK", "tiempo_respuesta_ms": 1658},
        "riesgo": {"puntaje": 18, "senales": []},
        "version": "2.1"
    }
)
session.add(trans)
session.commit()
```

### 💻 Consultar con SQLAlchemy

```python
# Acceder a JSONB
trans = session.query(Transaccion).filter(
    Transaccion.id_transaccion == 'TXN-2024-001'
).first()

banco = trans.autorizacion['emisor']['nombre']
puntaje = trans.autorizacion['riesgo']['puntaje']
```

### 💻 Filtrar con JSONB

```python
# Filtrar por contenido
rechazadas = session.query(Transaccion).filter(
    Transaccion.autorizacion['rechazo']['codigo'].astext == 'FONDOS_INSUFICIENTES'
).all()

# Filtrar con @>
rechazadas = session.query(Transaccion).filter(
    Transaccion.autorizacion.op('@>')('{"rechazo":{"codigo":"FONDOS_INSUFICIENTES"}}')
).all()
```

---

## 9. RESUMEN

### 📌 Lecciones Clave

1. **JSONB** es más eficiente que JSON para lectura e índices.
2. **Operadores** `->`, `->>`, `#>`, `#>>` permiten acceder a datos anidados.
3. **Operador de contención** `@>` permite búsquedas rápidas.
4. **Índices GIN** aceleran las búsquedas en JSONB.
5. **SQLAlchemy 2.0** permite mapear JSONB a objetos Python.
6. **Caso de uso:** Mensajes de autorización de pagos.

### 🎯 Frase para Recordar

> *"JSONB en PostgreSQL te da lo mejor de dos mundos: la flexibilidad de un documento NoSQL con la potencia de una base de datos relacional."*

---

**¿El profesor mencionó algún ejemplo específico de mensaje de autorización con JSONB?** 🚀📓