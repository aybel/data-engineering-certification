# 📓 WORKBOOK - SESIÓN 1.2
## Ingesta Robusta y Diseño de Landing Zone - Pipelines y ETL con Python

**Curso:** Pipelines y ETL con Python | BSG Institute
**Fecha:** 01/10/2026
**Duración:** [pendiente] (Sesión 2 de 14)

---

## 📌 ÍNDICE

1. [Panorama de la Sesión](#1-panorama-de-la-sesión)
2. [Las Seis Preguntas Antes de Ingestar](#2-las-seis-preguntas-antes-de-ingestar)
3. [Diseño de Landing Zone](#3-diseño-de-landing-zone)
4. [Metadatos en la Landing Zone](#4-metadatos-en-la-landing-zone)
5. [Ingesta de Archivos con Contratos de Datos](#5-ingesta-de-archivos-con-contratos-de-datos)
6. [Ingesta desde APIs: Paginación y Rate Limiting](#6-ingesta-desde-apis-paginación-y-rate-limiting)
7. [Reintentos con Backoff (Retry Pattern)](#7-reintentos-con-backoff-retry-pattern)
8. [Trampas en CSV: Mojibake](#8-trampas-en-csv-mojibake)
9. [Código, Configuración y Secretos (Operación)](#9-código-configuración-y-secretos-operación)
10. [Buenas Prácticas Aplicadas a la Ingesta](#10-buenas-prácticas-aplicadas-a-la-ingesta)
11. [Conexión con la Sesión 1.1](#11-conexión-con-la-sesión-11)
12. [Resumen de la Sesión](#12-resumen-de-la-sesión)

---

## 1. PANORAMA DE LA SESIÓN

### 🎯 Idea Central

> *"La ingesta no es solo 'traer datos': es traerlos de forma robusta, repetible, segura y respetuosa con las fuentes."*

Esta sesión construye la **primera pieza real del pipeline**: la **ingesta** hacia la **landing zone** (el punto de entrada de los datos crudos, antes de Bronze).

### 📋 Los Temas de la Sesión

| # | Tema | Qué resuelve |
|---|------|--------------|
| 1 | **Las 6 preguntas** | Diseño previo antes de escribir código |
| 2 | **Landing Zone y Metadatos** | Dónde y cómo aterrizan los datos crudos con trazabilidad |
| 3 | **Archivos con contratos** | Validar la estructura esperada de un archivo |
| 4 | **APIs (Paginación y Rate Limit)** | Traer datos de APIs sin abusar ni perder páginas |
| 5 | **Reintentos con backoff** | Recuperarse de fallas temporales |
| 6 | **Mojibake y trampas CSV** | Evitar basura silenciosa por encodings |
| 7 | **Código/Config/Secretos** | Escribir ingesta mantenible y segura |

---

## 2. LAS SEIS PREGUNTAS ANTES DE INGESTAR

> *"Antes de escribir una sola línea de código de ingesta, hay que responder seis preguntas. Cada una define una decisión de diseño."*

| # | Pregunta | Qué define | Implicación |
|---|----------|------------|-------------|
| **1** | **¿De quién es la fuente?** | Dueño, contacto y a quién avisar cuando cambie | Gobernanza y comunicación |
| **2** | **¿Cada cuánto cambia?** | Frecuencia y si conviene incremental | Estrategia de ingesta |
| **3** | **¿Completa o incremental?** | ¿Traigo todo o solo lo nuevo? | Volumen y costo |
| **4** | **¿Cuánto volumen?** | Filas por día, tamaño de archivo, límites de la API | Diseño técnico |
| **5** | **¿Hay contrato?** | Esquema, formato y reglas acordadas por escrito | Validación |
| **6** | **¿Datos sensibles?** | Datos personales o financieros | Cifrado y acceso mínimo |

### 📌 Regla de Oro

> **"Ninguna ingesta debe empezar sin responder las seis preguntas. Si no sabes qué traes, cuánto, cada cuándo, con qué reglas y con qué sensibilidad, no estás listo para ingestar."**

---

## 3. DISEÑO DE LANDING ZONE

> *"La landing zone es la puerta de entrada del pipeline: aquí aterrizan los datos crudos, tal como llegan, sin transformar."*

### 🏗️ Ubicación en la Arquitectura

```
FUENTES  →  LANDING ZONE  →  🥉 BRONZE  →  🥈 SILVER  →  🥇 GOLD  →  CONSUMIDORES
           (aterrizaje)     (crudo)       (limpio)      (negocio)
```

> 💡 **Clave:** La landing zone y Bronze no son lo mismo. La landing zone es el recién llegado (a veces temporal); Bronze es el dato ya consolidado y preservado a largo plazo.

### 🔑 Principios de Diseño

| Principio | Descripción |
|-----------|-------------|
| **Inmutable** | Los datos se depositan y no se modifican; si hay corrección, se agrega otra versión |
| **Organizada por tiempo** | Particionada por fecha/hora de ingesta (ej. `landing/2026-10-01/pedidos.json`) |
| **Trazable** | Se sabe de dónde vino, cuándo llegó y con qué parámetros |
| **Separada por fuente** | Cada fuente en su propia ruta (`postgres/`, `api_catalogo/`, `csv_proveedores/`) |
| **Reprocesable** | Se puede volver a leer para reprocesar sin tocar la fuente |
| **Barata** | Almacenamiento tipo object storage (S3, GCS, disco local) |

### 🗂️ Estructura Típica

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

### ✅ Anti-patrones

| Anti-patrón | Problema |
|-------------|----------|
| Todo en una sola carpeta | Imposible saber origen ni fecha |
| Archivos sobreescritos | Se pierde el histórico |
| Nombres tipo `datos_final_v2_ok.csv` | Sin estructura, sin trazabilidad |
| Datos transformados en landing | Rompe el principio de "crudo" |

---

## 4. METADATOS EN LA LANDING ZONE

> *"Los archivos sin metadatos son solo bytes. Los metadatos son los que convierten una carpeta en una landing zone de verdad."*

### 📖 ¿Qué son los Metadatos?

Son **datos sobre los datos**: describen qué es cada archivo, de dónde vino, cuándo llegó, cómo llegó y en qué estado está.

### 📋 Metadatos Mínimos por Archivo

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `archivo` | Nombre del archivo | `pedidos_20261001_0300.parquet` |
| `fuente` | Sistema de origen | `postgres_pedidos` |
| `fecha_ingesta` | Cuándo se ingestó | `2026-10-01T03:00:12Z` |
| `filas` | Cuántos registros trae | `15234` |
| `hash` | Checksum para detectar cambios | `sha256:abc123...` |
| `contrato` | Contrato aplicado | `contratos/pedidos.yaml` |
| `estado` | Resultado | `ok`, `cuarentena`, `error` |

### 💻 Manifiesto de Metadatos (JSON)

```json
{
  "archivo": "pedidos_20261001_0300.parquet",
  "fuente": "postgres_pedidos",
  "fecha_ingesta": "2026-10-01T03:00:12Z",
  "filas": 15234,
  "hash": "sha256:abc123...",
  "contrato": "contratos/pedidos.yaml",
  "estado": "ok"
}
```

> 💡 **Clave:** El manifiesto se guarda como un sidecar (`.meta.json`) junto al archivo. Cuando el pipeline crece, estos manifiestos se consolidan en un **Catálogo de Metadatos** (DataHub, Unity Catalog, Glue, etc.).

---

## 5. INGESTA DE ARCHIVOS CON CONTRATOS DE DATOS

> *"Un archivo no llega 'así nomás': llega con un contrato que dice qué columnas, qué tipos y qué reglas debe cumplir."*

### 🎯 Elementos de un Contrato

| Elemento | Qué define | Ejemplo |
|----------|-----------|---------|
| **Esquema** | Columnas y tipos | `pedido_id: int`, `monto: float` |
| **Obligatoriedad** | Columnas requeridas | `pedido_id` no puede faltar |
| **Rangos** | Valores válidos | `monto > 0` |
| **Formato** | Fecha, encoding, delimitador | `fecha` ISO 8601, UTF-8, `,` |

### 💻 Ejemplo: Contrato en Python (Pandera)

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

contrato_pedidos.validate(df)
```

### 🚦 ¿Qué Hacer si No Cumple?

| Opción | Cuándo usarla |
|--------|---------------|
| **Fail-fast** | El archivo es crítico y no debe entrar mal |
| **Cuarentena** | Guardar el archivo malo aparte para revisión |
| **Alertar** | Notificar sin detener el pipeline |

---

## 6. INGESTA DESDE APIS: PAGINACIÓN Y RATE LIMITING

> *"Una API no te da todo de una vez: te da páginas. Y no te deja pedir todo seguido: te pone un límite de tasa."*

### 📄 Paginación

| Tipo | Cómo funciona |
|------|---------------|
| **Offset / Limit** | `?offset=0&limit=100`, luego `offset=100` |
| **Cursor** | La API devuelve un `next_cursor` |
| **Token** | Cada respuesta trae un token para la siguiente |

```python
def traer_todas_las_paginas(base_url, params=None):
    resultados = []
    offset = 0
    limit = 100
    while True:
        peticion = {**params, "offset": offset, "limit": limit}
        resp = requests.get(base_url, params=peticion, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        resultados.extend(data["items"])
        
        if len(data["items"]) < limit:
            break
        offset += limit
    return resultados
```

### 🚦 Rate Limiting

| Cabecera | Significado |
|----------|-------------|
| `X-RateLimit-Limit` | Máximo de peticiones permitidas |
| `X-RateLimit-Remaining` | Peticiones restantes |
| `Retry-After` | Segundos a esperar tras un 429 |

> 💡 **Clave:** Ser respetuoso con la API (código 429) no es solo buena educación: es requisito para que no te bloqueen.

---

## 7. REINTENTOS CON BACKOFF (RETRY PATTERN)

> *"Las fallas temporales son normales. Un pipeline robusto no se rinde al primer error: reintenta con inteligencia."*

### 🔄 Tipos de Backoff

| Tipo | Cómo espera | Ejemplo (segundos) |
|------|-------------|--------------------|
| **Fixed** | Siempre el mismo tiempo | 5, 5, 5, 5 |
| **Linear** | Aumenta de forma constante | 5, 10, 15, 20 |
| **Exponential** | Duplica el tiempo | 1, 2, 4, 8, 16 |
| **Exponential + Jitter** | Exponential + aleatoriedad | 1.2, 2.5, 3.9, 8.7 |

> 💡 **Clave:** El **jitter** evita el efecto *thundering herd* (que múltiples instancias reintenten al mismo tiempo y saturen la fuente).

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
            time.sleep(espera)
```

---

## 8. TRAMPAS EN CSV: MOJIBAKE

> *"El mojibake es el error más traicionero: los datos se ven casi bien, hasta que los miras de cerca."*

### 🔍 Ejemplo Visual

| Original (UTF-8) | Mojibake (leído como Latin-1) |
|------------------|-------------------------------|
| `José` | `JosÃ©` |
| `México` | `MÃ©xico` |
| `€` (euro) | `â‚¬` |

> 💡 **Clave:** El mojibake **no lanza error**. El archivo se lee "bien", pero los datos quedan corruptos.

### 🛠️ Cómo Prevenir y Detectar

| Práctica | Aplicación |
|----------|------------|
| **Declarar el encoding** | `pd.read_csv(..., encoding="utf-8")` |
| **Exigir UTF-8 en el contrato** | Que el proveedor entregue UTF-8 |
| **Detectar con `chardet`** | Analizar los primeros KB del archivo |

```python
import chardet
with open("inventario.csv", "rb") as f:
    muestra = f.read(100_000)
    enc = chardet.detect(muestra)["encoding"]
```

### 🪤 Otras Trampas Comunes en CSV

| Trampa | Defensa |
|--------|---------|
| **BOM inesperado** | `encoding="utf-8-sig"` |
| **Delimitador distinto (`;`)** | `csv.Sniffer()` |
| **Tipos inferidos mal (`"01"` → `1`)** | `dtype=str` |
| **Nulos disfrazados (`"N/A"`, `"-"`)** | `na_values=[...]` |

> 💡 **Clave:** Lee el CSV como si fuera hostil. La lectura defensiva es la diferencia entre "funciona en mi máquina" y "funciona en producción".

---

## 9. CÓDIGO, CONFIGURACIÓN Y SECRETOS (OPERACIÓN)

> *"Tres capas, tres destinos, tres reglas. Ninguna se mezcla con las otras."*

### 📊 Las Tres Capas

| Capa | Qué contiene | Dónde vive | ¿Va a Git? |
|------|--------------|------------|------------|
| 💻 **Código** | La lógica: cómo se lee, valida y escribe | `ingesta/*.py` | ✅ Sí |
| ⚙️ **Configuración** | Lo que cambia entre ambientes: rutas, URLs, parámetros | `config.yaml` | ✅ Sí |
| 🔑 **Secretos** | Llaves, contraseñas, tokens | `.env` | ❌ **NUNCA** |

### 🗺️ ¿Dónde Vive el Secreto?

| Entorno | Dónde vive |
|---------|------------|
| **Local** | `.env` + `python-dotenv` |
| **Colab** | Panel de Secretos de Colab |
| **Google Cloud** | **Secret Manager** |
| **AWS** | **Secrets Manager** |

### 🚨 REGLA CRÍTICA: SI LLEGÓ A GIT, YA SE FILTRÓ

> *"Si un secreto llegó a git, ya se filtró: rótalo, no basta con borrarlo del repositorio."*

**¿Por qué borrarlo no basta?**
- El historial de commits conserva el secreto.
- Los clones y forks ya lo tienen.
- Los bots de GitHub escanean repositorios en segundos.

**Qué hacer:**
1. **Rotar el secreto inmediatamente** (cambiar la contraseña/token).
2. Auditar accesos con esa credencial.
3. Reescribir historial (`git filter-repo`) *después* de rotar.
4. Prevenir con `pre-commit` y `gitleaks`.

---

## 10. BUENAS PRÁCTICAS APLICADAS A LA INGESTA

| Práctica | Aplicación en la ingesta |
|----------|--------------------------|
| 🔁 **Idempotente** | Traer la misma página dos veces no duplica; se sobrescribe la partición |
| 🔄 **Reprocesable** | Landing zone preserva todo → se puede reprocesar cualquier día |
| 🧱 **Atómico** | El archivo se escribe completo o no se escribe (temp + rename) |
| 👁️ **Observable** | Logs por página, métricas de reintentos, alertas de contrato roto |
| 🧪 **Probado** | Tests de contrato con archivos de ejemplo; tests de paginación con mocks |
| 🔒 **Seguro** | Secretos inyectados, TLS con APIs, PII cifrada en landing |

---

## 11. CONEXIÓN CON LA SESIÓN 1.1

| Concepto Sesión 1.1 | Cómo se concreta en la Sesión 1.2 |
|---------------------|-----------------------------------|
| **Pipeline de datos** | Se construye la primera etapa: la ingesta |
| **Ciclo de vida (Reis & Housley)** | Se trabaja la etapa de **Ingesta** |
| **Arquitectura Medallion** | Se prepara la antesala de Bronze: la landing zone |
| **Caso integrador (tienda en línea)** | Se definen los conectores de las cuatro fuentes |
| **Buenas prácticas** | Se aplican idempotencia, seguridad y observabilidad a la ingesta |

---

## 12. RESUMEN DE LA SESIÓN

### 📌 Lecciones Aprendidas

1. **Las seis preguntas:** Antes de ingestar, define dueño, frecuencia, tipo (completa/incremental), volumen, contrato y sensibilidad.
2. **Landing zone:** Es la puerta de entrada inmutable y organizada por fecha/fuente. No es lo mismo que Bronze.
3. **Metadatos:** Son los sidecars (`.meta.json`) que dan trazabilidad, auditoría y permiten la idempotencia.
4. **Contratos de datos:** Validan esquema, tipos y reglas. Si fallan, se aplica cuarentena o fail-fast.
5. **APIs:** Requieren paginación (offset, cursor) y respeto al rate limit (429 y `Retry-After`).
6. **Backoff:** Reintentos exponenciales con jitter para manejar fallas temporales sin saturar la fuente.
7. **Mojibake y CSV:** No confíes en el encoding por defecto. Usa `chardet` y lectura defensiva.
8. **Secretos:** Si un secreto llega a Git, ya se filtró. Rótalo y usa gestores como Secret Manager.
9. **Separación:** Código y configuración van a Git; los secretos se inyectan en runtime.

### 🗂️ Estructura Conceptual de la Ingesta

```
🔌 INGESTA (Sesión 1.2)
├── 🔍 6 Preguntas de Diseño
├── 📥 Landing Zone (inmutable, particionada)
│   └── 🏷️ Metadatos (.meta.json)
├── 📄 Contratos de datos (esquema, tipos, reglas)
├── 🌐 APIs (paginación, rate limiting)
├── 🔁 Reintentos (backoff exponencial + jitter)
├── 🪤 Defensa CSV (encoding, delimitadores, nulos)
└── 🗂️ Separación de capas (código, config, secretos)
```

### 🎯 Preparado para la Próxima Sesión

- ✅ Diseño de ingesta claro (6 preguntas)
- ✅ Landing zone y metadatos documentados
- ✅ Contratos de datos implementados con Pandera
- ✅ Patrón de paginación y rate limiting entendido
- ✅ Backoff con jitter documentado
- ✅ Lectura defensiva de CSV (mojibake)
- ✅ Separación código/config/secretos establecida
- ⏳ Pendiente: Implementación práctica de los conectores

---

**Nota final:** *"La ingesta es la primera impresión del pipeline: si entra mal, todo lo que sigue arrastra el error. Diseñar bien la landing zone, respetar las APIs y separar código, config y secretos es lo que hace que el pipeline aguante el mundo real."*

---