# 📓 WORKBOOK - SESIÓN 13
## MongoDB y el Modelo Documental

**Curso:** Bases de Datos y SQL con Python | BSG Institute  
**Fecha:** 22/09/2026  
**Duración:** 2 horas

---

## 📌 ÍNDICE

- [📓 WORKBOOK - SESIÓN 13](#-workbook---sesión-13)
  - [MongoDB y el Modelo Documental](#mongodb-y-el-modelo-documental)
  - [📌 ÍNDICE](#-índice)
  - [1. VOCABULARIO: SQL VS MONGODB](#1-vocabulario-sql-vs-mongodb)
  - [2. EL ENTORNO](#2-el-entorno)
  - [3. LA DECISIÓN CENTRAL: UNA OPERACIÓN, DOS FORMAS](#3-la-decisión-central-una-operación-dos-formas)
  - [4. DENORMALIZACIÓN: INCORPORAR EN LUGAR DE REFERENCIAR](#4-denormalización-incorporar-en-lugar-de-referenciar)
    - [💻 Documento MongoDB](#-documento-mongodb)
  - [5. CONSULTAR: EL FILTRO ES UN DICCIONARIO](#5-consultar-el-filtro-es-un-diccionario)
    - [💻 Ejemplos de consultas](#-ejemplos-de-consultas)
  - [6. EQUIVALENCIAS SQL VS PYMONGO](#6-equivalencias-sql-vs-pymongo)
  - [7. ESCRIBIR: EL ERROR QUE NO FALLA](#7-escribir-el-error-que-no-falla)
    - [💻 Operaciones de escritura](#-operaciones-de-escritura)
  - [8. ESQUEMA FLEXIBLE: QUÉ VALIDA CADA MOTOR](#8-esquema-flexible-qué-valida-cada-motor)
  - [9. EL PUNTO DE LA SESIÓN: UN MONTO QUE NO ES UN NÚMERO](#9-el-punto-de-la-sesión-un-monto-que-no-es-un-número)
    - [💻 Demostración](#-demostración)
  - [10. DIAGNÓSTICO: SABER QUÉ HAY DENTRO](#10-diagnóstico-saber-qué-hay-dentro)
    - [💻 Consultas de diagnóstico](#-consultas-de-diagnóstico)
  - [11. LA CONTRAPARTIDA: LO QUE CUESTA HABER INCORPORADO](#11-la-contrapartida-lo-que-cuesta-haber-incorporado)
  - [12. GARANTÍAS: QUÉ SÍ APLICA EL MOTOR](#12-garantías-qué-sí-aplica-el-motor)
  - [13. CIERRE: LO QUE QUEDA PLANTEADO](#13-cierre-lo-que-queda-planteado)
  - [14. HERRAMIENTAS: MONGOSH, COMPASS Y DOCKER](#14-herramientas-mongosh-compass-y-docker)
    - [📌 MONGOSH (MongoDB Shell)](#-mongosh-mongodb-shell)
    - [📌 COMPASS (Interfaz Gráfica)](#-compass-interfaz-gráfica)
    - [📌 DOCKER: MongoDB](#-docker-mongodb)
  - [15. CONEXIÓN DESDE PYTHON CON PYMONGO](#15-conexión-desde-python-con-pymongo)
    - [📌 CONEXIÓN BÁSICA](#-conexión-básica)
    - [📌 CONEXIÓN CON VARIABLES DE ENTORNO](#-conexión-con-variables-de-entorno)
  - [16. OPERACIONES CRUD CON PYMONGO](#16-operaciones-crud-con-pymongo)
    - [1. INSERTAR](#1-insertar)
    - [2. CONSULTAR](#2-consultar)
    - [3. ACTUALIZAR](#3-actualizar)
    - [4. ELIMINAR](#4-eliminar)
  - [17. AGREGACIONES CON PYMONGO](#17-agregaciones-con-pymongo)
    - [💻 Canalización de Agregación](#-canalización-de-agregación)
    - [📊 Operadores de Agregación](#-operadores-de-agregación)
  - [18. MATERIALES DE LA SESIÓN](#18-materiales-de-la-sesión)
  - [📝 FICHA DE MONGODB (En construcción)](#-ficha-de-mongodb-en-construcción)
  - [⚠️ ERRORES COMUNES CON PYMONGO](#️-errores-comunes-con-pymongo)
  - [🎯 RESUMEN](#-resumen)

---

## 1. VOCABULARIO: SQL VS MONGODB

> *"Lo mismo con otros nombres."*

| SQL | MongoDB |
|-----|---------|
| base de datos | base de datos |
| tabla | colección |
| fila | documento |
| columna | campo |
| llave primaria | `_id` |
| esquema declarado con DDL | no hay |

> 💡 **Clave:** La última fila es la única diferencia real. No existe `CREATE COLLECTION`: la colección nace con el primer documento insertado.

---

## 2. EL ENTORNO

> *"Los dos motores conviven. PostgreSQL no se apaga: el capítulo 3 lee de él y la sesión 3.3 los compara."*

---

## 3. LA DECISIÓN CENTRAL: UNA OPERACIÓN, DOS FORMAS

> *"Cinco tablas con cuatro combinaciones, o un documento autosuficiente."*

---

## 4. DENORMALIZACIÓN: INCORPORAR EN LUGAR DE REFERENCIAR

### 💻 Documento MongoDB

```python
{
  "_id": "TRX0000010",
  "monto": 3553.02,
  "estatus": "APROBADA",
  "comercio": { "id": 4, "nombre": "Boutique Iris", "ciudad": "Ciudad de Mexico" },
  "cliente":  { "id": 88, "nombre": "Patricia Gonzalez", "correo": "..." },
  "tarjeta":  { "id": 102, "ultimos4": "4417", "marca": "VISA" },
  "autorizacion": { ... }
}
```

> 💡 **Clave:** El comercio y el cliente se **incorporan** al documento. Leer la operación completa es una sola búsqueda.

> ⚠️ **Nota:** Se conservan también los identificadores de origen. Permiten volver al modelo relacional y son la única vía para corregir un dato en todas las operaciones.

---

## 5. CONSULTAR: EL FILTRO ES UN DICCIONARIO

### 💻 Ejemplos de consultas

```python
coleccion.find({"comercio.ciudad": "Merida"})                # notacion de punto
coleccion.find({"monto": {"$gt": 20000}})                    # comparacion
coleccion.find({"tarjeta.marca": {"$in": ["AMEX", "VISA"]}}) # lista
coleccion.find({"autorizacion.riesgo": {"$exists": True}})   # existencia
coleccion.find({"estatus": "APROBADA", "monto": {"$gt": 100}})  # Y implicito
```

> ⚠️ **Advertencia:** `{"comercio": {"nombre": "X"}}` no equivale a `{"comercio.nombre": "X"}`. El primero busca un subdocumento exactamente igual, con esos campos y en ese orden. Devuelve cero y no produce error.

> 💡 **Clave:** Es la confusión más frecuente al empezar, y es silenciosa.

---

## 6. EQUIVALENCIAS SQL VS PYMONGO

| SQL | PyMongo |
|-----|---------|
| `SELECT cols FROM t WHERE f` | `find(f, cols)` |
| `ORDER BY c DESC` | `.sort("c", DESCENDING)` |
| `LIMIT n` / `OFFSET n` | `.limit(n)` / `.skip(n)` |
| `COUNT(*)` | `count_documents(f)` |
| `IN (...)` | `{"$in": [...]}` |
| `GROUP BY` | `{"$group": {...}}` en la canalización |

> 💡 **Nota:** Una diferencia útil: el puntaje de riesgo se guardó como número dentro del documento, de modo que la comparación no requiere conversión. En la sesión 2.4 con `->>` hacía falta convertir a entero.

---

## 7. ESCRIBIR: EL ERROR QUE NO FALLA

### 💻 Operaciones de escritura

```python
# Modifica el estatus y deja el resto intacto
coleccion.update_one({"_id": "TRX001"}, {"$set": {"estatus": "REVERSADA"}})

# SUSTITUYE el documento entero. El monto y la moneda desaparecen.
coleccion.replace_one({"_id": "TRX001"}, {"estatus": "REVERSADA"})
```

| Operación | Campos que quedan |
|-----------|-------------------|
| `update_one` con `$set` | todos |
| `replace_one` sin `$set` | 2 |

> ⚠️ **Advertencia:** La segunda operación reporta éxito. El documento queda mutilado y nada lo advierte.

> 💡 **Regla:** `update_one` con `$set` salvo que la intención explícita sea reemplazar el documento completo.

---

## 8. ESQUEMA FLEXIBLE: QUÉ VALIDA CADA MOTOR

> *"La flexibilidad y el riesgo son la misma propiedad."*

---

## 9. EL PUNTO DE LA SESIÓN: UN MONTO QUE NO ES UN NÚMERO

### 💻 Demostración

```python
coleccion.insert_one({"_id": "X", "monto": "mil pesos", "estatus": "APROBADA"})
# aceptado

coleccion.aggregate([{"$group": {"_id": None, "suma": {"$sum": "$monto"}}}])
# suma: 10,105,599.87     documentos considerados: 3918
```

> ⚠️ **Advertencia:** `$sum` **ignora** los valores que no son numéricos. No falla, no advierte, y el documento sí se cuenta en el total. La suma es incorrecta y nada lo delata.

> 💡 **Clave:** En PostgreSQL, la columna `NUMERIC` habría rechazado el valor al insertarlo. Es el contraste más directo entre los dos capítulos.

---

## 10. DIAGNÓSTICO: SABER QUÉ HAY DENTRO

### 💻 Consultas de diagnóstico

```python
coleccion.count_documents({"monto": {"$type": "string"}})
coleccion.count_documents({"monto": {"$not": {"$type": "number"}}})

coleccion.aggregate([
    {"$group": {"_id": {"$type": "$monto"}, "cuantos": {"$sum": 1}}}])
```

> 💡 **Nota:** `$type` revela qué tipos conviven en un mismo campo. En una colección sin validación de esquema, es la única forma de saberlo.

> 💡 **Clave:** Conviene tratarlo como práctica de higiene, no como curiosidad. La validación de esquema, que recupera parte del control, se ve en la sesión 3.2.

---

## 11. LA CONTRAPARTIDA: LO QUE CUESTA HABER INCORPORADO

| Operación | PostgreSQL | MongoDB |
|-----------|------------|---------|
| Leer una operación completa | 4 combinaciones | 1 búsqueda |
| Importe por comercio | 2 combinaciones | agrupación directa |
| Corregir el nombre de un comercio | **1 fila** | **1524 documentos** |
| Esa corrección es atómica | sí | no, entre documentos |

> 💡 **Nota:** En la sesión 1.2, el problema del archivo plano era justamente que el nombre del comercio se repetía en cada fila. La normalización lo resolvió.

> 💡 **Clave:** El modelo documental reintroduce esa redundancia **a propósito**. La diferencia de intención es lo que separa un modelo mal hecho de una denormalización informada.

---

## 12. GARANTÍAS: QUÉ SÍ APLICA EL MOTOR

| ✅ Sí garantiza | ❌ No garantiza |
|----------------|----------------|
| `_id` único en la colección | Que un campo exista |
| La escritura de un documento es atómica | Que un campo tenga un tipo determinado |
| Los tipos de BSON se conservan al leer | Que un valor pertenezca a un dominio |
| | Que una referencia a otra colección resuelva |

> 💡 **Nota:** Los tres primeros de la derecha se recuperan en parte con validación de esquema, en la sesión 3.2. El cuarto no tiene equivalente: no existen llaves foráneas.

> 💡 **Clave:** MongoDB ofrece transacciones multidocumento desde la versión 4, con requisitos de configuración.

---

## 13. CIERRE: LO QUE QUEDA PLANTEADO

- El documento incorpora lo que el modelo relacional referenciaba
- Leer no paga combinaciones; escribir paga redundancia
- El motor no valida estructura, tipos ni dominios
- Un dato mal tipado entra en los cálculos sin producir error

> 💡 **Pregunta que abre la sesión 3.2:** Si el motor no valida nada, ¿cómo se responde una pregunta analítica sobre datos que pueden venir de cualquier forma, y con qué herramientas se hace con eficiencia?

> 📝 **Trabajo para la próxima sesión:** Partes A a E del taller, e iniciar la ficha de seis puntos de MongoDB.

---

## 14. HERRAMIENTAS: MONGOSH, COMPASS Y DOCKER

### 📌 MONGOSH (MongoDB Shell)

**¿Qué es?** La shell oficial de MongoDB para ejecutar comandos desde la terminal.

**Instalación:**
```bash
# Windows (con winget)
winget install MongoDB.Shell

# macOS (con Homebrew)
brew install mongosh
```

**Conexión:**
```bash
mongosh "mongodb://datacourse:datacourse123@localhost:27017"
```

**Comandos básicos:**
```javascript
// Ver bases de datos
show dbs

// Usar una base de datos
use dataengineering

// Ver colecciones
show collections

// Consultar documentos
db.transacciones.find({estatus: "APROBADA"}).limit(5)

// Contar documentos
db.transacciones.countDocuments()

// Insertar
db.transacciones.insertOne({...})

// Actualizar
db.transacciones.updateOne({_id: "TRX001"}, {$set: {estatus: "REVERSADA"}})

// Eliminar
db.transacciones.deleteOne({_id: "TRX001"})
```

---

### 📌 COMPASS (Interfaz Gráfica)

**¿Qué es?** La interfaz gráfica oficial de MongoDB para explorar datos visualmente.

**Descarga:** https://www.mongodb.com/try/download/compass

**Conexión:**
```
mongodb://datacourse:datacourse123@localhost:27017
```

**Ventajas:**
- Ver documentos en formato JSON legible
- Ejecutar consultas visualmente
- Explorar esquemas automáticamente
- Ver estadísticas de rendimiento
- Crear índices visualmente

---

### 📌 DOCKER: MongoDB

**Archivo `docker-compose.yml`:**
```yaml
services:
  mongodb:
    image: mongo:7.0
    container_name: curso_mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGODB_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_PASSWORD}
      MONGO_INITDB_DATABASE: ${MONGODB_DB}
    ports:
      - "${MONGODB_PORT:-27017}:27017"
    volumes:
      - mongodata:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  mongodata:
```

**Comandos Docker:**
```bash
# Levantar
docker compose up -d mongodb

# Ver estado
docker compose ps

# Ver logs
docker compose logs -f mongodb

# Entrar al contenedor
docker exec -it curso_mongodb mongosh

# Detener
docker compose down
```

---

## 15. CONEXIÓN DESDE PYTHON CON PYMONGO

> *"PyMongo es el driver oficial de MongoDB para Python."*

### 📌 CONEXIÓN BÁSICA

```python
from pymongo import MongoClient

# 1. CONECTAR (con credenciales)
cliente = MongoClient(
    "mongodb://datacourse:datacourse123@localhost:27017"
)

# 2. SELECCIONAR BASE DE DATOS
db = cliente["dataengineering"]

# 3. SELECCIONAR COLECCIÓN
coleccion = db["transacciones"]

# 4. VERIFICAR CONEXIÓN
print(cliente.list_database_names())
print(db.list_collection_names())
```

### 📌 CONEXIÓN CON VARIABLES DE ENTORNO

```python
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

cliente = MongoClient(
    host=os.getenv("MONGODB_HOST", "localhost"),
    port=int(os.getenv("MONGODB_PORT", 27017)),
    username=os.getenv("MONGODB_USER"),
    password=os.getenv("MONGODB_PASSWORD")
)

db = cliente[os.getenv("MONGODB_DB", "dataengineering")]
coleccion = db["transacciones"]

print("✅ Conectado a MongoDB")
```

---

## 16. OPERACIONES CRUD CON PYMONGO

### 1. INSERTAR

```python
# Insertar un documento
documento = {
    "_id": "TRX0000010",
    "monto": 3553.02,
    "estatus": "APROBADA",
    "comercio": {"id": 4, "nombre": "Boutique Iris", "ciudad": "Ciudad de Mexico"},
    "cliente": {"id": 88, "nombre": "Patricia Gonzalez"},
    "tarjeta": {"id": 102, "ultimos4": "4417", "marca": "VISA"}
}

coleccion.insert_one(documento)

# Insertar varios
coleccion.insert_many([doc1, doc2, doc3])
```

### 2. CONSULTAR

```python
# Buscar uno
doc = coleccion.find_one({"_id": "TRX0000010"})

# Buscar varios
for doc in coleccion.find({"estatus": "APROBADA"}):
    print(doc)

# Con filtros
coleccion.find({"monto": {"$gt": 20000}})
coleccion.find({"comercio.ciudad": "Merida"})
coleccion.find({"tarjeta.marca": {"$in": ["AMEX", "VISA"]}})

# Con proyección (solo algunos campos)
coleccion.find({}, {"_id": 1, "monto": 1, "estatus": 1})

# Con ordenamiento
from pymongo import DESCENDING
coleccion.find().sort("monto", DESCENDING)

# Con límite
coleccion.find().limit(10)

# Contar
coleccion.count_documents({"estatus": "APROBADA"})
```

### 3. ACTUALIZAR

```python
# Actualizar un campo (sin borrar el resto)
coleccion.update_one(
    {"_id": "TRX0000010"},
    {"$set": {"estatus": "REVERSADA"}}
)

# Actualizar varios
coleccion.update_many(
    {"comercio.ciudad": "Merida"},
    {"$set": {"comercio.zona": "Sureste"}}
)

# Incrementar un valor
coleccion.update_one(
    {"_id": "TRX0000010"},
    {"$inc": {"intentos": 1}}
)

# Agregar a un array
coleccion.update_one(
    {"_id": "TRX0000010"},
    {"$push": {"senales": "MONTO_ALTO"}}
)
```

### 4. ELIMINAR

```python
# Eliminar uno
coleccion.delete_one({"_id": "TRX0000010"})

# Eliminar varios
coleccion.delete_many({"estatus": "RECHAZADA"})

# Eliminar toda la colección
coleccion.delete_many({})
```

---

## 17. AGREGACIONES CON PYMONGO

### 💻 Canalización de Agregación

```python
# Importe por comercio
resultado = coleccion.aggregate([
    {"$match": {"estatus": "APROBADA"}},
    {"$group": {"_id": "$comercio.nombre", "importe": {"$sum": "$monto"}}},
    {"$sort": {"importe": -1}}
])

for doc in resultado:
    print(doc)
```

### 📊 Operadores de Agregación

| Operador | Función | Equivalente SQL |
|----------|---------|-----------------|
| `$match` | Filtra documentos | `WHERE` |
| `$group` | Agrupa | `GROUP BY` |
| `$sort` | Ordena | `ORDER BY` |
| `$limit` | Limita | `LIMIT` |
| `$skip` | Salta | `OFFSET` |
| `$project` | Selecciona campos | `SELECT` |
| `$sum` | Suma | `SUM` |
| `$avg` | Promedio | `AVG` |
| `$min` / `$max` | Mínimo / Máximo | `MIN` / `MAX` |
| `$count` | Cuenta | `COUNT` |

---

## 18. MATERIALES DE LA SESIÓN

| Archivo | Contenido |
|---------|-----------|
| `c3_s1_b0_diagramas.py` | Render de las tres figuras |
| `c3_s1_b1_preparacion.md` | Contenedor de MongoDB y verificación |
| `c3_s1_b2_docker_compose.yml` | Definición del servicio |
| `c3_s1_b2_env_ejemplo.txt` | Variables que se agregan al `.env` existente |
| `c3_s1_b3_carga.py` | De PostgreSQL a MongoDB, con la denormalización |
| `c3_s1_b4_operaciones.py` | Consulta, inserción, actualización y borrado |
| `c3_s1_b5_taller.md` | Taller evaluable |

---

## 📝 FICHA DE MONGODB (En construcción)

| # | Punto | MongoDB |
|---|-------|---------|
| **1** | **Modelo de datos que asume** | Documental (documentos BSON en colecciones) |
| **2** | **Operaciones eficientes** | Lectura de documentos completos, agregaciones |
| **3** | **Garantías de consistencia** | `_id` único, atomicidad a nivel documento |
| **4** | **Costo escritura vs lectura** | Lectura barata (sin joins); escritura costosa (redundancia) |
| **5** | **Interfaz desde Python** | `pymongo` (MongoClient) |
| **6** | **Conviene / No conviene** | ✅ Datos variables, logs, perfiles<br>❌ Datos con relaciones complejas, validación estricta |

---

## ⚠️ ERRORES COMUNES CON PYMONGO

| Error | Causa | Solución |
|-------|-------|----------|
| `ServerSelectionTimeoutError` | No se puede conectar al servidor | Verificar que MongoDB esté corriendo |
| `DuplicateKeyError` | `_id` duplicado | Usar otro `_id` o `upsert=True` |
| `OperationFailure` | Operación no permitida | Verificar permisos del usuario |
| `Documento mutilado` | Usar `replace_one` sin `$set` | Usar `update_one` con `$set` |
| `Suma incorrecta` | Datos no numéricos en `$sum` | Validar tipos con `$type` |

---

## 🎯 RESUMEN

| Operación | PyMongo |
|-----------|---------|
| **Conectar** | `MongoClient(...)` |
| **Insertar** | `insert_one()`, `insert_many()` |
| **Consultar** | `find_one()`, `find()` |
| **Actualizar** | `update_one()`, `update_many()` |
| **Eliminar** | `delete_one()`, `delete_many()` |
| **Agregar** | `aggregate([...])` |
| **Contar** | `count_documents()` |

---

**¿El profesor mostró cómo cargar los datos desde PostgreSQL a MongoDB?** 🚀📓