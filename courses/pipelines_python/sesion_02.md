# 📓 WORKBOOK - SESIÓN 1.2
## Diseño de Landing Zone e Ingesta Robusta - Pipelines y ETL con Python

**Curso:** Pipelines y ETL con Python | BSG Institute
**Fecha:** 01/10/2026
**Duración:** [2 hrs] (Sesión 2 de 14)

---

## 📌 ÍNDICE

1. [Panorama de la Sesión](#1-panorama-de-la-sesión)
2. [Diseño de Landing Zone](#2-diseño-de-landing-zone)
3. [Ingesta de Archivos con Contratos de Datos](#3-ingesta-de-archivos-con-contratos-de-datos)
4. [Ingesta desde APIs: Paginación y Rate Limiting](#4-ingesta-desde-apis-paginación-y-rate-limiting)
5. [Reintentos con Backoff (Retry Pattern)](#5-reintentos-con-backoff-retry-pattern)
6. [Separación de Código, Configuración y Secretos](#6-separación-de-código-configuración-y-secretos)
7. [Buenas Prácticas Aplicadas a la Ingesta](#7-buenas-prácticas-aplicadas-a-la-ingesta)
8. [Conexión con la Sesión 1.1](#8-conexión-con-la-sesión-11)
9. [Resumen de la Sesión](#9-resumen-de-la-sesión)

---

## 1. PANORAMA DE LA SESIÓN

### 🎯 Idea Central

> *"La ingesta no es solo 'traer datos': es traerlos de forma robusta, repetible, segura y respetuosa con las fuentes."*

Esta sesión construye la **primera pieza real del pipeline**: la **ingesta** hacia la **landing zone** (el punto de entrada de los datos crudos, antes de Bronze).

### 📋 Los Cinco Temas de la Sesión

| # | Tema | Qué resuelve |
|---|------|--------------|
| 1 | **Diseño de Landing Zone** | Dónde y cómo aterrizan los datos crudos |
| 2 | **Archivos con contratos** | Cómo validar la estructura esperada de un archivo |
| 3 | **APIs con paginación y rate limiting** | Cómo traer datos de APIs sin abusar ni perder páginas |
| 4 | **Reintentos con backoff** | Cómo recuperarse de fallas temporales |
| 5 | **Separar código, configuración y secretos** | Cómo escribir ingesta mantenible y segura |

> 💡 **Clave:** Estos cinco temas son la diferencia entre un script frágil que "trae datos" y una ingesta de producción.

---

## 2. DISEÑO DE LANDING ZONE

> *"La landing zone es la puerta de entrada del pipeline: aquí aterrizan los datos crudos, tal como llegan, sin transformar."*

### 📖 ¿Qué es una Landing Zone?

Es la **zona de aterrizaje** del pipeline: el lugar (carpeta, bucket, tabla) donde se depositan los datos **recién extraídos de las fuentes**, antes de cualquier transformación. Es la antesala de la capa Bronze.

### 🏗️ Ubicación en la Arquitectura

```
FUENTES  →  LANDING ZONE  →  🥉 BRONZE  →  🥈 SILVER  →  🥇 GOLD  →  CONSUMIDORES
           (aterrizaje)     (crudo)       (limpio)      (negocio)
```

> 💡 **Clave:** La landing zone y Bronze pueden parecer iguales, pero **no lo son**:
> - **Landing zone:** recién llegado, tal cual, a veces temporal.
> - **Bronze:** ya consolidado, organizado, preservado a largo plazo.

### 🔑 Principios de Diseño de una Landing Zone

| Principio | Descripción |
|-----------|-------------|
| **Inmutable** | Los datos se depositan y **no se modifican**; si hay corrección, se agrega otra versión |
| **Organizada por tiempo** | Particionada por fecha/hora de ingesta (ej. `landing/2026-10-01/pedidos.json`) |
| **Trazable** | Se puede saber **de dónde vino**, **cuándo llegó** y **con qué parámetros** |
| **Separada por fuente** | Cada fuente en su propia ruta (`postgres/`, `api_catalogo/`, `csv_proveedores/`) |
| **Reprocesable** | Se puede volver a leer para reprocesar sin tocar la fuente original |
| **Barata** | Almacenamiento tipo object storage (S3, GCS, disco local) |

### 🗂️ Estructura Típica de una Landing Zone

```
landing/
├── postgres/
│   └── pedidos/
│       └── 2026-10-01/
│           └── pedidos_20261001_0300.parquet
├── api_catalogo/
│   └── 2026-10-01/
│       └── page_0001.json ... page_0050.json
├── csv_proveedores/
│   └── 2026-10-01/
│       └── inventario_20261001.csv
└── eventos/
    └── 2026-10-01/
        └── clics_20261001_0000.jsonl
```

### 🔑 Convenciones de Nombres

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| **Fuente** | minúsculas, guion bajo | `api_catalogo` |
| **Entidad** | singular | `pedido`, `cliente`, `inventario` |
| **Fecha** | ISO 8601 (`YYYY-MM-DD`) | `2026-10-01` |
| **Hora** | `HHMM` si aplica | `0300` |
| **Extensión** | según formato | `.parquet`, `.json`, `.csv`, `.jsonl` |

### ✅ Anti-patrones de Landing Zone

| Anti-patrón | Problema |
|-------------|----------|
| Todo en una sola carpeta | Imposible saber origen ni fecha |
| Archivos sobreescritos | Se pierde el histórico |
| Nombres tipo `datos_final_v2_ok.csv` | Sin estructura, sin trazabilidad |
| Datos transformados en landing | Rompe el principio de "crudo" |
| Sin separación por fuente | Reprocesar una fuente afecta a otras |

### 📌 Regla de Oro

> **"La landing zone es un archivo histórico inmutable de lo que llegó, cuándo y de dónde."**

---

## 3. INGESTA DE ARCHIVOS CON CONTRATOS DE DATOS

> *"Un archivo no llega 'así nomás': llega con un contrato que dice qué columnas, qué tipos y qué reglas debe cumplir."*

### 📖 ¿Qué es un Contrato de Datos?

Es un **acuerdo explícito** (documento o código) que define la **estructura y reglas** que un archivo debe cumplir. Si el archivo no cumple, la ingesta **falla rápido** o se marca para cuarentena.

### 🎯 ¿Por Qué Usar Contratos?

| Razón | Beneficio |
|-------|-----------|
| **Detectar cambios de esquema** | Si el proveedor agrega/quita columnas, lo sabemos al instante |
| **Evitar datos corruptos en Bronze** | Solo entra lo que cumple el contrato |
| **Facilitar validaciones automáticas** | El contrato es la fuente de verdad de las reglas |
| **Documentar acuerdos con proveedores** | Claro qué se espera de cada archivo |

### 📋 Elementos de un Contrato de Datos

| Elemento | Qué define | Ejemplo |
|----------|-----------|---------|
| **Esquema** | Columnas y tipos | `pedido_id: int`, `monto: float`, `fecha: date` |
| **Obligatoriedad** | Columnas requeridas | `pedido_id` no puede faltar |
| **Tipos** | Tipo de cada columna | `monto` debe ser numérico |
| **Rangos** | Valores válidos | `monto > 0` |
| **Formato** | Formato de fecha, encoding, delimitador | `fecha` en ISO 8601, UTF-8, `,` |
| **Unicidad** | Columnas clave | `pedido_id` único |
| **Frecuencia** | Cuándo se espera | Diario a las 03:00 |

### 💻 Ejemplo: Contrato en Python (con Pandera)

```python
import pandera as pa
from pandera import Column, Check, DataFrameSchema

contrato_pedidos = DataFrameSchema({
    "pedido_id": Column(int, Check.greater_than(0), unique=True),
    "cliente_id": Column(int, Check.greater_than(0)),
    "monto": Column(float, Check.greater_than(0)),
    "fecha": Column("datetime64[ns]"),
    "estado": Column(str, Check.isin(["pagado", "pendiente", "cancelado"])),
})

# Validar antes de subir a la landing zone
contrato_pedidos.validate(df)
```

### 💻 Ejemplo: Contrato en YAML (declarativo)

```yaml
# contratos/pedidos.yaml
nombre: pedidos
fuente: csv_proveedores
columnas:
  - nombre: pedido_id
    tipo: int
    requerido: true
    unico: true
  - nombre: cliente_id
    tipo: int
    requerido: true
  - nombre: monto
    tipo: float
    requerido: true
    min: 0.01
  - nombre: fecha
    tipo: date
    formato: "%Y-%m-%d"
  - nombre: estado
    tipo: string
    valores: [pagado, pendiente, cancelado]
```

### 🚦 ¿Qué Hacer Cuando un Archivo No Cumple el Contrato?

| Opción | Cuándo usarla |
|--------|---------------|
| **Fail-fast** | El archivo es crítico y no debe entrar mal |
| **Cuarentena** | Guardar el archivo malo aparte para revisión |
| **Alertar** | Notificar al equipo sin detener el pipeline |
| **Registrar y continuar** | Cuando la regla es "blanda" |

> 💡 **Clave:** El contrato **no es solo validación**: es un **acuerdo documentado** entre quien produce el dato y quien lo consume.

---

## 4. INGESTA DESDE APIS: PAGINACIÓN Y RATE LIMITING

> *"Una API no te da todo de una vez: te da páginas. Y no te deja pedir todo seguido: te pone un límite de tasa."*

### 🎯 Los Dos Retos de las APIs

| Reto | Qué es | Consecuencia si se ignora |
|------|--------|---------------------------|
| **Paginación** | Los datos vienen por páginas | Se pierde información |
| **Rate limiting** | Límite de peticiones por tiempo | Bloqueo temporal o permanente de la IP/API key |

---

### 📄 4.1 Paginación

> *"Traer todas las páginas hasta que la API diga 'no hay más'."*

#### 🔑 Tipos Comunes de Paginación

| Tipo | Cómo funciona | Ejemplo |
|------|---------------|---------|
| **Offset / Limit** | `?offset=0&limit=100`, luego `offset=100` | APIs clásicas |
| **Page / Per page** | `?page=1&per_page=100` | APIs REST comunes |
| **Cursor** | La API devuelve un `next_cursor` | GitHub, Stripe |
| **Link header** | Header `Link: <...>; rel="next"` | APIs estilo HATEOAS |
| **Token** | Cada respuesta trae un token para la siguiente | APIs paginadas token-based |

#### 💻 Patrón de Ingesta con Paginación (offset/limit)

```python
import requests

def traer_todas_las_paginas(base_url, params=None):
    params = params or {}
    resultados = []
    offset = 0
    limit = 100

    while True:
        peticion = {**params, "offset": offset, "limit": limit}
        resp = requests.get(base_url, params=peticion, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        resultados.extend(data["items"])

        # Condición de parada: la API devolvió menos de `limit`
        if len(data["items"]) < limit:
            break
        offset += limit

    return resultados
```

> ⚠️ **Apunte clave:** La condición de parada depende del tipo de paginación. Nunca asumas que "siempre hay más": verifica el `total`, el `next`, o cuántos vinieron en la última página.

---

### 🚦 4.2 Rate Limiting

> *"La API te dice cuántas peticiones puedes hacer por minuto. Si te pasas, te bloquea."*

#### 🔑 Cabeceras Típicas de Rate Limiting

| Cabecera | Significado |
|----------|-------------|
| `X-RateLimit-Limit` | Máximo de peticiones permitidas |
| `X-RateLimit-Remaining` | Peticiones que te quedan |
| `X-RateLimit-Reset` | Cuándo se reinicia el contador |
| `Retry-After` | Segundos a esperar tras un 429 |

#### 🚨 Código HTTP 429: Too Many Requests

| Código | Significado | Acción |
|--------|-------------|--------|
| **429** | Demasiadas peticiones | Esperar `Retry-After` y reintentar |
| **403** | Prohibido | Revisar credenciales o permisos |
| **500 / 502 / 503** | Error del servidor | Reintentar con backoff |
| **408** | Timeout | Reintentar |

#### 💻 Patrón: Respetar el Rate Limit

```python
import time
import requests

def peticion_respetuosa(url, params=None, max_reintentos=5):
    for intento in range(max_reintentos):
        resp = requests.get(url, params=params, timeout=30)

        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 429:
            espera = int(resp.headers.get("Retry-After", 5))
            print(f"Rate limit alcanzado. Esperando {espera}s...")
            time.sleep(espera)
            continue

        resp.raise_for_status()

    raise RuntimeError("Se agotaron los reintentos")
```

> 💡 **Clave:** Ser **respetuoso con la API** no es solo buena educación: es requisito para que no te bloqueen y para que el pipeline sea confiable.

---

## 5. REINTENTOS CON BACKOFF (RETRY PATTERN)

> *"Las fallas temporales son normales. Un pipeline robusto no se rinde al primer error: reintenta con inteligencia."*

### 📖 ¿Qué es un Reintento con Backoff?

Es la estrategia de **volver a intentar una operación fallida**, esperando **cada vez más tiempo** entre intentos, para no saturar la fuente ni el propio pipeline.

### 🔄 Tipos de Backoff

| Tipo | Cómo espera | Ejemplo (segundos) |
|------|-------------|--------------------|
| **Fixed** | Siempre el mismo tiempo | 5, 5, 5, 5 |
| **Linear** | Aumenta de forma constante | 5, 10, 15, 20 |
| **Exponential** | Duplica el tiempo | 1, 2, 4, 8, 16 |
| **Exponential + Jitter** | Exponential + aleatoriedad | 1.2, 2.5, 3.9, 8.7 |

> 💡 **Clave:** El **jitter** (aleatoriedad) evita que múltiples instancias reintenten **al mismo tiempo** y saturen la fuente (efecto *thundering herd*).

### 🛠️ ¿Cuándo Reintentar y Cuándo No?

| ✅ Reintentar | ❌ No reintentar |
|--------------|------------------|
| Error de red (timeout, DNS) | Error 400 (petición mal formada) |
| Error 500, 502, 503 | Error 401 / 403 (credenciales) |
| Error 429 (rate limit) | Error 404 (recurso no existe) |
| Fuente temporalmente caída | Datos que no cumplen contrato |

### 💻 Patrón: Retry con Backoff Exponencial

```python
import time
import random
import requests

def con_backoff(func, max_intentos=5, base=1.0, max_espera=60):
    for intento in range(max_intentos):
        try:
            return func()
        except (requests.Timeout, requests.ConnectionError) as e:
            if intento == max_intentos - 1:
                raise
            espera = min(base * (2 ** intento), max_espera)
            espera += random.uniform(0, 0.5)  # jitter
            print(f"Falla temporal: {e}. Reintento en {espera:.2f}s")
            time.sleep(espera)
```

### 🔁 Backoff vs. Backfill

| Concepto | Qué significa |
|----------|---------------|
| **Retry (backoff)** | Volver a intentar una operación **fallida** |
| **Backfill** | Reprocesar datos de **periodos pasados** de forma intencional |

> 💡 **Nota:** En la sesión el profesor mencionó "reintento de backfill". Son dos mecanismos distintos que se complementan: el backoff maneja fallas temporales; el backfill reprocesa periodos que faltan o están mal.

### 📌 Regla de Oro

> **"Reintentar sin backoff es solo insistir. Reintentar con backoff es ingeniería."**

---

## 6. SEPARACIÓN DE CÓDIGO, CONFIGURACIÓN Y SECRETOS

> *"El código no debe saber dónde está la base de datos, ni la contraseña, ni cuántas páginas traer. Eso va aparte."*

### 🎯 Los Tres Niveles

| Nivel | Qué contiene | Dónde vive |
|-------|--------------|------------|
| **Código** | La lógica (cómo hacer las cosas) | Repositorio Git |
| **Configuración** | Parámetros (URLs, rutas, límites, nombres) | Archivos `.env`, `.yaml`, variables de entorno |
| **Secretos** | Credenciales (passwords, tokens, API keys) | Gestor de secretos (Vault, Secret Manager, GitHub Secrets) |

### 🔑 ¿Por Qué Separarlos?

| Razón | Beneficio |
|-------|-----------|
| **Seguridad** | Los secretos no van al repositorio |
| **Portabilidad** | Mismo código en dev, staging, prod con distinta config |
| **Mantenibilidad** | Cambiar un parámetro no implica tocar código |
| **Auditoría** | Sabes quién cambió qué y cuándo |
| **Cumplimiento** | Requisito en industrias reguladas (PCI, HIPAA) |

### ❌ Anti-patrón: Todo Hardcodeado

```python
# ❌ MAL: credenciales y parámetros en el código
conn = psycopg2.connect(
    host="prod-db.empresa.com",
    user="admin",
    password="SuperSecreta123!",  # ¡Esto nunca debe estar aquí!
    dbname="pedidos"
)
LIMITE_API = 100
URL_API = "https://api.tienda.com/v1/pedidos"
```

### ✅ Patrón Correcto: Código + Config + Secretos

```python
# ✅ BIEN: código limpio, config y secretos separados
import os
from dotenv import load_dotenv

load_dotenv()  # carga variables desde .env (no versionado)

conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],  # inyectado desde el gestor de secretos
    dbname=os.environ["DB_NAME"],
)
LIMITE_API = int(os.environ.get("API_LIMIT", 100))
URL_API = os.environ["API_URL"]
```

### 📁 Estructura Recomendada de un Proyecto de Ingesta

```
proyecto_ingesta/
├── src/
│   ├── ingestores/
│   │   ├── postgres.py
│   │   ├── api_catalogo.py
│   │   ├── csv_proveedores.py
│   │   └── eventos.py
│   ├── utilidades/
│   │   ├── retry.py
│   │   ├── contratos.py
│   │   └── landing.py
│   └── main.py
├── config/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── prod.yaml
├── contratos/
│   ├── pedidos.yaml
│   ├── clientes.yaml
│   └── inventario.yaml
├── .env.example         # plantilla, SÍ va al repo
├── .env                 # valores reales, NO va al repo
├── .gitignore           # ignora .env y secretos
└── README.md
```

### 🔒 Buenas Prácticas con Secretos

| Práctica | Detalle |
|----------|---------|
| **Nunca en Git** | `.env` en `.gitignore`, secretos en gestor |
| **Nunca en logs** | No imprimir tokens ni passwords |
| **Rotación periódica** | Cambiar credenciales regularmente |
| **Mínimo privilegio** | Cada servicio con solo los permisos que necesita |
| **Cifrado** | Secretos cifrados en reposo y en tránsito |
| **Auditoría** | Saber quién accede a qué secreto y cuándo |

### 📌 Regla de Oro

> **"El código se comparte, la configuración se versiona por entorno, y los secretos se inyectan. Nunca se mezclan."**

---

## 7. BUENAS PRÁCTICAS APLICADAS A LA INGESTA

Cómo se aplican las **seis buenas prácticas de la Sesión 1.1** al trabajo de esta sesión:

| Práctica | Aplicación en la ingesta |
|----------|--------------------------|
| 🔁 **Idempotente** | Traer la misma página dos veces no duplica en landing; se sobrescribe la partición |
| 🔄 **Reprocesable** | Landing zone preserva todo → se puede reprocesar cualquier día |
| 🧱 **Atómico** | El archivo se escribe completo o no se escribe (escritura temp + rename) |
| 👁️ **Observable** | Logs por página, métricas de reintentos, alertas de contrato roto |
| 🧪 **Probado** | Tests de contrato con archivos de ejemplo; tests de paginación con mocks |
| 🔒 **Seguro** | Secretos inyectados, TLS con APIs, PII cifrada en landing |

---

## 8. CONEXIÓN CON LA SESIÓN 1.1

| Concepto Sesión 1.1 | Cómo se concreta en la Sesión 1.2 |
|---------------------|-----------------------------------|
| **Pipeline de datos** | Se construye la primera etapa: la ingesta |
| **Ciclo de vida (Reis & Housley)** | Se trabaja la etapa de **Ingesta** |
| **Arquitectura Medallion** | Se prepara la antesala de Bronze: la landing zone |
| **Caso integrador (tienda en línea)** | Se definen los conectores de las cuatro fuentes |
| **Buenas prácticas** | Se aplican idempotencia, seguridad, observabilidad a la ingesta |
| **Ficha de 6 puntos** | La ingesta es donde más se nota el **punto 5** (interfaz desde Python) |

---

## 9. RESUMEN DE LA SESIÓN

### 📌 Lecciones Aprendidas

1. **Landing zone** es la puerta de entrada del pipeline: inmutable, organizada por tiempo y fuente, y separada de Bronze.
2. **Los archivos llegan con contrato**: esquema, tipos, reglas y unicidad se validan antes de aterrizar.
3. **Las APIs requieren respeto**: paginación para no perder datos, rate limiting para no ser bloqueados.
4. **Reintentos con backoff**: exponential + jitter es el estándar para fallas temporales.
5. **Backoff ≠ backfill**: uno maneja fallas temporales, el otro reprocesa periodos pasados.
6. **Código, configuración y secretos se separan**: el código se versiona, la config se parametriza, los secretos se inyectan.
7. Los cinco temas aplican directamente las **buenas prácticas** de la Sesión 1.1.

### 🗂️ Estructura Conceptual de la Ingesta

```
🔌 INGESTA (Sesión 1.2)
├── 📥 Landing Zone
│   ├── inmutable
│   ├── particionada por fecha
│   └── separada por fuente
├── 📄 Contratos de datos
│   ├── esquema
│   ├── tipos y rangos
│   └── unicidad y formato
├── 🌐 APIs
│   ├── paginación (offset, cursor, link)
│   └── rate limiting (429, Retry-After)
├── 🔁 Reintentos
│   ├── backoff exponencial
│   └── jitter
└── 🗂️ Separación de capas
    ├── código (src/)
    ├── configuración (config/)
    └── secretos (env / vault)
```

### 🎯 Preparado para la Próxima Sesión

- ✅ Landing zone diseñada
- ✅ Contratos de datos entendidos
- ✅ Patrón de paginación y rate limiting documentado
- ✅ Backoff con jitter internalizado
- ✅ Separación código/config/secretos clara
- ⏳ Pendiente: implementación concreta de los cuatro conectores

---

**Nota final:** *"La ingesta es la primera impresión del pipeline: si entra mal, todo lo que sigue arrastra el error. Diseñar bien la landing zone, respetar las APIs y separar código, config y secretos es lo que hace que el pipeline aguante el mundo real."*

---