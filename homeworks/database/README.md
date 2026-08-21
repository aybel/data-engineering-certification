# 📓 excerciseS - SESIÓN 1.1
## Bases de Datos y SQL con Python | SQLite

**Curso:** Bases de Datos y SQL con Python | BSG Institute  
**Fecha:** 11/08/2026  
**excercises:** 10 excercises del nivel básico al avanzado

---

## 📊 MAPA DE DIFICULTAD

| Ejercicio | Nivel | Conceptos |
|-----------|-------|-----------|
| 1 | 🟢 Básico | Conexión, CREATE TABLE |
| 2 | 🟢 Básico | INSERT, commit |
| 3 | 🟢 Básico | SELECT, WHERE, fetchall |
| 4 | 🟡 Intermedio | UPDATE, parámetros |
| 5 | 🟡 Intermedio | DELETE, SELECT |
| 6 | 🟡 Intermedio | JOIN, ALTER TABLE |
| 7 | 🟡 Intermedio | Agregaciones, fetchone |
| 8 | 🟠 Avanzado | GROUP BY, HAVING |
| 9 | 🟠 Avanzado | Subconsultas |
| 10 | 🔴 Proyecto | Todo lo anterior integrado |

---

## 🔹 EJERCICIO 1: Conexión Básica a SQLite

**Nivel:** 🟢 Básico  
**Objetivo:** Establecer una conexión a una base de datos SQLite y crear una tabla.

### Instrucciones

1. Importa el módulo `sqlite3`
2. Conéctate a una base de datos llamada `tienda.db`
3. Crea una tabla llamada `productos` con las siguientes columnas:
   - `id INTEGER PRIMARY KEY AUTOINCREMENT`
   - `nombre TEXT NOT NULL`
   - `precio REAL`
   - `stock INTEGER`
4. Cierra la conexión

## 🔹 EJERCICIO 2: Insertar Datos
**Nivel:** 🟢 Básico
**Objetivo:** Insertar registros en una tabla SQLite.

### Instrucciones

1. Conéctate a `tienda.db`
2. Inserta los siguientes productos en la tabla `productos`:

- "Laptop", 15000.00, 10
- "Mouse", 250.00, 50
- "Teclado", 450.00, 30
3. Confirma los cambios con `commit()`
4. Cuenta cuántos productos hay en la tabla
5. Muestra el resultado

### Código Base
```python
import sqlite3

# Tu código aquí
```

### Pistas

- Usa `cursor.execute()` con `INSERT INTO`
- Usa `cursor.fetchone()` para obtener el COUNT
- Recuerda el `commit()`

---

## 🔹 EJERCICIO 3: Consultar Datos
**Nivel:** 🟢 Básico
**Objetivo:** Consultar datos de una tabla con filtros.

### Instrucciones

1. Conéctate a `tienda.db`
2. Consulta todos los productos con precio mayor a 300
3. Muestra los resultados en formato de tabla
4. Cierra la conexión

### Código Base
```python
import sqlite3

# Tu código aquí
```

### Pistas

- Usa `SELECT * FROM productos WHERE precio > 300`
- Usa `fetchall()` para obtener todos los resultados
- Recorre los resultados con un `for`

---

## 🔹 EJERCICIO 4: Actualizar Datos
**Nivel:** 🟡 Intermedio
**Objetivo:** Actualizar registros en una tabla.

### Instrucciones

1. Conéctate a `tienda.db`
2. Actualiza el precio del producto "Mouse" a 280.00
3. Confirma los cambios
4. Consulta el producto actualizado para verificar
5. Muestra el resultado

### Código Base
```python
import sqlite3

# Tu código aquí
```

### Pistas

- Usa `UPDATE productos SET precio = ? WHERE nombre = ?`
- Usa parámetros en `execute()`

---

## 🔹 EJERCICIO 5: Eliminar Datos
**Nivel:** 🟡 Intermedio
**Objetivo:** Eliminar registros de una tabla.

### Instrucciones

1. Conéctate a `tienda.db`
2. Elimina el producto con id = 2
3. Confirma los cambios
4. Consulta todos los productos restantes
5. Muestra cuántos quedaron

### Código Base
```python
import sqlite3

# Tu código aquí
```

### Pistas

- Usa `DELETE FROM productos WHERE id = ?`
- Usa `fetchall()` para ver los resultados

---

## 🔹 EJERCICIO 6: Consultas con JOIN
**Nivel:** 🟡 Intermedio
**Objetivo:** Trabajar con múltiples tablas y JOINs.

### Instrucciones

1. Conéctate a `tienda.db`
2. Crea una tabla `categorias` con:

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `nombre TEXT NOT NULL`
3. Inserta categorías: "Electrónicos", "Accesorios", "Periféricos"
4. Agrega una columna `categoria_id` a la tabla `productos`
5. Actualiza los productos con su categoría correspondiente
6. Consulta productos con su categoría usando JOIN
7. Muestra los resultados

### Código Base
```python
import sqlite3

# Tu código aquí
```

### Pistas

- Usa `ALTER TABLE` para agregar la columna
- Usa `UPDATE` para asignar categorías
- Usa `INNER JOIN` para la consulta

---

## 🔹 EJERCICIO 7: Funciones de Agregación
**Nivel:** 🟡 Intermedio
**Objetivo:** Usar funciones de agregación en SQL.

### Instrucciones

1. Conéctate a `tienda.db`
2. Calcula:

- Cantidad total de productos (`COUNT`)
- Precio promedio (`AVG`)
- Precio máximo (`MAX`)
- Precio mínimo (`MIN`)
- Valor total del inventario (`SUM(precio * stock)`)
3. Muestra los resultados

### Código Base
```python
import sqlite3

# Tu código aquí
```

### Pistas

- Usa `SELECT COUNT(*)`, `AVG(precio)`, etc.
- Usa `fetchone()` para obtener los valores

---

## 🔹 EJERCICIO 8: GROUP BY y HAVING
**Nivel:** 🟠 Avanzado
**Objetivo:** Agrupar datos y filtrar grupos con HAVING.

### Instrucciones

1. Conéctate a `tienda.db`
2. Agrupa productos por categoría
3. Calcula:

- Cantidad de productos por categoría
- Precio promedio por categoría
4. Filtra solo categorías con precio promedio > 500
5. Muestra los resultados

### Código Base
```python
import sqlite3

# Tu código aquí
```

### Pistas

- Usa `GROUP BY categoria_id`
- Usa `HAVING AVG(precio) > 500`

---

## 🔹 EJERCICIO 9: Subconsultas
**Nivel:** 🟠 Avanzado
**Objetivo:** Escribir subconsultas en SQL.

### Instrucciones

1. Conéctate a `tienda.db`
2. Encuentra:

- Productos con precio mayor al promedio
- La categoría con más productos
3. Usa subconsultas para ambas consultas
4. Muestra los resultados

### Código Base
```python
import sqlite3

# Tu código aquí
```

### Pistas

- Subconsulta en WHERE: `WHERE precio > (SELECT AVG(precio) FROM productos)`
- Subconsulta en FROM o con JOIN

---

## 🔹 EJERCICIO 10: Proyecto Integrador
**Nivel:** 🔴 Proyecto
**Objetivo:** Aplicar todos los conceptos en un caso completo.

### Instrucciones

1. Crea un script completo que:

- Cree la base de datos `tienda.db`
- Cree todas las tablas necesarias (productos, categorías)
- Inserte datos de prueba (al menos 10 productos de 3 categorías)
- Ejecute las siguientes consultas:
a) Todos los productos ordenados por precio
b) Productos con stock bajo (< 20)
c) Resumen por categoría (cantidad, precio promedio)
d) Producto más caro y más barato por categoría
e) Top 3 productos más caros
- Muestre los resultados de forma clara

### Código Base
```python
import sqlite3

def main():
    # Tu código aquí
    pass

if __name__ == "__main__":
    main()
```

### Pistas

- Organiza tu código en funciones
- Usa `CREATE TABLE IF NOT EXISTS`
- Inserta datos con `executemany()` para mayor eficiencia
- Usa `ORDER BY`, `GROUP BY`, `JOIN`, `HAVING`
- Documenta tu código con comentarios

---

## 💡 RECOMENDACIONES FINALES

1. **Orden:** Resuelve los ejercicios en orden del 1 al 10
2. **Pruebas:** Ejecuta tu código después de cada cambio
3. **Errores:** Lee los mensajes de error, te ayudan a aprender
4. **Documentación:** Consulta [docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)
5. **Comparte:** Si tienes dudas, comparte tu código para recibir retroalimentación

---
**¡Buena suerte y a programar! 🚀🐍**

```text
¡Listo! Todos los ejercicios en un solo `README.md` dentro de la carpeta `homeworks/database/` 📚🚀
```