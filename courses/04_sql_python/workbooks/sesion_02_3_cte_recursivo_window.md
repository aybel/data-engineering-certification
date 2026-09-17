# 📓 WORKBOOK - SESIÓN 9
## Subconsultas, CTEs y Funciones de Ventana

**Curso:** Bases de Datos y SQL con Python | BSG Institute
**Fecha:** 10/09/2026
**Duración:** 2 horas

---

## 📌 ÍNDICE

- [📓 WORKBOOK - SESIÓN 9](#-workbook---sesión-9)
  - [Subconsultas, CTEs y Funciones de Ventana](#subconsultas-ctes-y-funciones-de-ventana)
  - [📌 ÍNDICE](#-índice)
  - [1. PROCESAMIENTO EN EL SERVIDOR](#1-procesamiento-en-el-servidor)
  - [2. GROUP BY VS FUNCIONES DE VENTANA](#2-group-by-vs-funciones-de-ventana)
    - [💻 Ejemplo](#-ejemplo)
  - [3. SUBCONSULTAS](#3-subconsultas)
    - [💻 Tipos](#-tipos)
  - [4. CTES](#4-ctes)
    - [💻 Sintaxis](#-sintaxis)
    - [💻 Ejemplo](#-ejemplo-1)
    - [💻 CTE Múltiple](#-cte-múltiple)
  - [5. FUNCIONES DE VENTANA](#5-funciones-de-ventana)
    - [💻 Sintaxis](#-sintaxis-1)
    - [💻 Ejemplo: Acumulado](#-ejemplo-acumulado)
  - [6. FUNCIONES DE RANKING](#6-funciones-de-ranking)
  - [7. NTILE Y CUARTILES](#7-ntile-y-cuartiles)
  - [8. LAG Y LEAD](#8-lag-y-lead)
  - [9. MARCOS DE VENTANA](#9-marcos-de-ventana)
  - [10. OPTIMIZACIÓN](#10-optimización)
  - [11. TIMEZONES](#11-timezones)
  - [12. EJERCICIOS](#12-ejercicios)
  - [13. RESUMEN](#13-resumen)
    - [📌 Lecciones Clave](#-lecciones-clave)
    - [🎯 Frase para Recordar](#-frase-para-recordar)

---

## 1. PROCESAMIENTO EN EL SERVIDOR

> *"Realizar operaciones de agregación y funciones de ventana directamente en el servidor de bases de datos (PostgreSQL) es más eficiente que extraer datos a Python."*

| Aspecto | SQL en Servidor | Pandas en Python |
|---------|-----------------|------------------|
| **Velocidad** | ✅ Optimizado | 🟡 Depende de RAM |
| **Memoria** | ✅ Solo resultados | ❌ Carga todo |
| **Escalabilidad** | ✅ Millones | ❌ Limitado por RAM |

---

## 2. GROUP BY VS FUNCIONES DE VENTANA

| Característica | GROUP BY | Funciones de Ventana |
|----------------|----------|---------------------|
| **Resultado** | Colapsa filas | Mantiene todas las filas |
| **Sintaxis** | `GROUP BY columna` | `OVER (PARTITION BY columna)` |
| **Uso** | Resúmenes | Acumulados, rankings |

### 💻 Ejemplo

```sql
-- GROUP BY (colapsa)
SELECT id_tarjeta, SUM(monto) AS total
FROM movimientos
GROUP BY id_tarjeta;

-- Función de ventana (mantiene detalle)
SELECT id_tarjeta, monto, fecha_hora,
       SUM(monto) OVER (PARTITION BY id_tarjeta) AS total_tarjeta
FROM movimientos;
```

---

## 3. SUBCONSULTAS

### 💻 Tipos

```sql
-- En WHERE
SELECT * FROM tarjetas
WHERE id IN (
    SELECT id_tarjeta FROM movimientos
    GROUP BY id_tarjeta HAVING COUNT(*) > 5
);

-- En FROM
SELECT AVG(total_ventas) AS promedio
FROM (
    SELECT comercio, SUM(monto) AS total_ventas
    FROM movimientos GROUP BY comercio
) AS subconsulta;

-- En SELECT
SELECT id_tarjeta, monto,
       (SELECT COUNT(*) FROM movimientos m2 WHERE m2.id_tarjeta = m1.id_tarjeta) AS total_tx
FROM movimientos m1;
```

---

## 4. CTES

### 💻 Sintaxis

```sql
WITH nombre_cte AS (
    SELECT ...
)
SELECT * FROM nombre_cte;
```

### 💻 Ejemplo

```sql
WITH ventas_por_comercio AS (
    SELECT comercio, SUM(monto) AS total_ventas
    FROM movimientos
    GROUP BY comercio
)
SELECT AVG(total_ventas) AS promedio
FROM ventas_por_comercio;
```

### 💻 CTE Múltiple

```sql
WITH
ventas_por_comercio AS (
    SELECT comercio, SUM(monto) AS total FROM movimientos GROUP BY comercio
),
promedio_ventas AS (
    SELECT AVG(total) AS promedio FROM ventas_por_comercio
)
SELECT * FROM promedio_ventas;
```

---

## 5. FUNCIONES DE VENTANA

### 💻 Sintaxis

```sql
funcion() OVER (
    PARTITION BY columna
    ORDER BY columna
    ROWS BETWEEN ...
)
```

### 💻 Ejemplo: Acumulado

```sql
SELECT
    id_tarjeta,
    fecha_hora,
    monto,
    SUM(monto) OVER (
        PARTITION BY id_tarjeta
        ORDER BY fecha_hora
    ) AS acumulado
FROM movimientos;
```

---

## 6. FUNCIONES DE RANKING

| Función | Comportamiento | Ejemplo |
|---------|----------------|---------|
| **ROW_NUMBER()** | Secuencial único | 1, 2, 3, 4, 5 |
| **RANK()** | Empates saltan | 1, 2, 2, 4, 5 |
| **DENSE_RANK()** | Empates no saltan | 1, 2, 2, 3, 4 |

```sql
SELECT
    cliente,
    COUNT(*) AS operaciones,
    ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS row_num,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS dense_rank
FROM movimientos
GROUP BY cliente;
```

---

## 7. NTILE Y CUARTILES

```sql
SELECT
    id_tarjeta,
    monto,
    NTILE(4) OVER (ORDER BY monto) AS cuartil
FROM movimientos;
```

---

## 8. LAG Y LEAD

| Función | Accede a |
|---------|----------|
| **LAG()** | Fila anterior |
| **LEAD()** | Fila siguiente |

```sql
SELECT
    id_tarjeta,
    fecha_hora,
    monto,
    LAG(monto) OVER (PARTITION BY id_tarjeta ORDER BY fecha_hora) AS monto_anterior,
    monto - LAG(monto) OVER (PARTITION BY id_tarjeta ORDER BY fecha_hora) AS diferencia
FROM movimientos;
```

---

## 9. MARCOS DE VENTANA

```sql
SELECT
    id_tarjeta,
    fecha_hora,
    monto,
    AVG(monto) OVER (
        PARTITION BY id_tarjeta
        ORDER BY fecha_hora
        ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
    ) AS promedio_movil
FROM movimientos;
```

---

## 10. OPTIMIZACIÓN

```sql
-- EXPLAIN ANALYZE
EXPLAIN ANALYZE
SELECT
    id_tarjeta,
    SUM(monto) OVER (PARTITION BY id_tarjeta ORDER BY fecha_hora)
FROM movimientos;

-- Índice para mejorar
CREATE INDEX idx_movimientos_tarjeta_fecha
ON movimientos (id_tarjeta, fecha_hora);
```

---

## 11. TIMEZONES

```sql
SELECT
    fecha_hora,
    fecha_hora AT TIME ZONE 'America/Mexico_City' AS fecha_mexico,
    fecha_hora AT TIME ZONE 'UTC' AS fecha_utc
FROM movimientos;
```

| Tipo | Descripción |
|------|-------------|
| **TIMESTAMP** | Sin zona horaria |
| **TIMESTAMPTZ** | Con zona horaria |

---

## 12. EJERCICIOS

```sql
-- 1. Acumulados por tarjeta
-- 2. Proporciones respecto al total
-- 3. Rankings de comercios
-- 4. Promedio móvil de 3 transacciones
-- 5. Diferencia entre transacciones consecutivas
```

---

## 13. RESUMEN

### 📌 Lecciones Clave

1. **Procesar en el servidor** es más eficiente.
2. **GROUP BY** colapsa filas, **funciones de ventana** mantienen detalle.
3. **CTEs** estructuran consultas complejas.
4. **Funciones de ventana** permiten acumulados, rankings y promedios móviles.
5. **LAG y LEAD** comparan filas anteriores y siguientes.
6. **EXPLAIN** ayuda a diagnosticar y optimizar.

### 🎯 Frase para Recordar

> *"El poder de SQL analítico está en procesar en el servidor lo que antes hacíamos en Python."*

---

**¿El profesor mencionó algún ejemplo específico con el caso de pagos?** 🚀📓