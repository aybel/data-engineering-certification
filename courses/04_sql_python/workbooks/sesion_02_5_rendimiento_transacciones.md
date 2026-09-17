# 📓 WORKBOOK - SESIONES 3 A 8
## Consultas SQL en SQLite

**Curso:** Bases de Datos y SQL con Python | BSG Institute
**Fecha:** 25/08/2026 - 08/09/2026

---

## 📌 TEMAS VISTOS

| Sesión | Tema | Conceptos |
|--------|------|-----------|
| **3** | Consultas con Filtros | `WHERE`, `ORDER BY`, operadores |
| **4** | Funciones de Agregación | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY` |
| **5** | Joins y Relaciones | `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN` |
| **6** | Subconsultas | Consultas anidadas |
| **7** | Vistas | `CREATE VIEW` |
| **8** | Índices y Optimización | `CREATE INDEX`, `EXPLAIN` |

---

## 1. CONSULTAS CON FILTROS

```sql
-- WHERE con operadores
SELECT * FROM movimientos WHERE monto > 1000;
SELECT * FROM movimientos WHERE estatus = 'APROBADA';
SELECT * FROM movimientos WHERE fecha_hora BETWEEN '2024-01-01' AND '2024-01-31';

-- ORDER BY
SELECT * FROM movimientos ORDER BY monto DESC;
SELECT * FROM movimientos ORDER BY fecha_hora ASC;
```

---

## 2. FUNCIONES DE AGREGACIÓN

```sql
-- COUNT, SUM, AVG, MIN, MAX
SELECT 
    COUNT(*) AS total,
    SUM(monto) AS suma,
    AVG(monto) AS promedio,
    MIN(monto) AS minimo,
    MAX(monto) AS maximo
FROM movimientos;

-- GROUP BY
SELECT comercio, COUNT(*) AS operaciones, SUM(monto) AS total
FROM movimientos
GROUP BY comercio
ORDER BY operaciones DESC;

-- HAVING
SELECT comercio, COUNT(*) AS operaciones
FROM movimientos
GROUP BY comercio
HAVING COUNT(*) > 10;
```

---

## 3. JOINS

```sql
-- INNER JOIN
SELECT m.id, c.nombre AS comercio, m.monto
FROM movimientos m
INNER JOIN comercios c ON m.comercio_id = c.id;

-- LEFT JOIN
SELECT c.nombre, COUNT(m.id) AS transacciones
FROM comercios c
LEFT JOIN movimientos m ON c.id = m.comercio_id
GROUP BY c.id, c.nombre;
```

---

## 4. SUBCONSULTAS

```sql
-- En WHERE
SELECT * FROM comercios
WHERE id IN (
    SELECT comercio_id FROM movimientos
    GROUP BY comercio_id HAVING COUNT(*) > 100
);

-- En FROM
SELECT AVG(total) AS promedio
FROM (
    SELECT comercio_id, SUM(monto) AS total
    FROM movimientos GROUP BY comercio_id
) AS subconsulta;
```

---

## 5. VISTAS

```sql
-- Crear vista
CREATE VIEW resumen_comercios AS
SELECT 
    c.nombre AS comercio,
    COUNT(m.id) AS transacciones,
    SUM(m.monto) AS total_ventas
FROM movimientos m
INNER JOIN comercios c ON m.comercio_id = c.id
GROUP BY c.id, c.nombre;

-- Usar vista
SELECT * FROM resumen_comercios WHERE total_ventas > 10000;
```

---

## 6. ÍNDICES

```sql
-- Crear índice
CREATE INDEX idx_movimientos_comercio ON movimientos(comercio_id);
CREATE INDEX idx_movimientos_fecha ON movimientos(fecha_hora);

-- Ver plan de ejecución
EXPLAIN ANALYZE SELECT * FROM movimientos WHERE comercio_id = 1;
```

---

## 📝 RESUMEN

| Sesión | Concepto Clave |
|--------|----------------|
| **3** | Filtros y ordenamiento |
| **4** | Agregaciones y agrupamiento |
| **5** | Joins entre tablas |
| **6** | Subconsultas anidadas |
| **7** | Vistas para simplificar consultas |
| **8** | Índices para optimizar |

---

**Estas sesiones fueron prácticas y no requirieron apuntes extensos.** 🚀📓