# 📓 WORKBOOK - SESIÓN 1.5 (Y CIERRE DEL CURSO)
## Orquestación con Apache Airflow - Pipelines y ETL con Python

**Curso:** Pipelines y ETL con Python | BSG Institute
**Fecha:** 13/11/2026
**Duración:** [pendiente] (Sesión 5 de 14 - Cierre del curso)

---

## 📌 ÍNDICE

- [📓 WORKBOOK - SESIÓN 1.5 (Y CIERRE DEL CURSO)](#-workbook---sesión-15-y-cierre-del-curso)
  - [Orquestación con Apache Airflow - Pipelines y ETL con Python](#orquestación-con-apache-airflow---pipelines-y-etl-con-python)
  - [📌 ÍNDICE](#-índice)
  - [1. PANORAMA: EL CASO INTEGRADOR CON AIRFLOW](#1-panorama-el-caso-integrador-con-airflow)
    - [🏗️ La Evolución del Pipeline](#️-la-evolución-del-pipeline)
    - [🕸️ La Anatomía del DAG `tienda_diaria`](#️-la-anatomía-del-dag-tienda_diaria)
  - [2. CRON VS. ORQUESTADOR](#2-cron-vs-orquestador)
  - [3. QUÉ HACE Y QUÉ NO HACE AIRFLOW](#3-qué-hace-y-qué-no-hace-airflow)
  - [4. ARQUITECTURA DE AIRFLOW 3](#4-arquitectura-de-airflow-3)
  - [5. LOS COMPONENTES DE AIRFLOW 3](#5-los-componentes-de-airflow-3)
  - [6. EL DAG MÍNIMO](#6-el-dag-mínimo)
  - [7. XCOM: LA REGLA DE ORO](#7-xcom-la-regla-de-oro)
  - [8. LOS ESTADOS DE UNA TAREA](#8-los-estados-de-una-tarea)
  - [9. LA FECHA LÓGICA: ¿QUÉ FECHA "ES" CADA CORRIDA?](#9-la-fecha-lógica-qué-fecha-es-cada-corrida)
  - [10. RESUMEN GENERAL DEL CURSO](#10-resumen-general-del-curso)
    - [🎓 El Viaje Completo de la Certificación](#-el-viaje-completo-de-la-certificación)
    - [📌 Las Reglas de Oro del Ingeniero de Datos](#-las-reglas-de-oro-del-ingeniero-de-datos)
    - [🎯 Próximos Pasos](#-próximos-pasos)

---

## 1. PANORAMA: EL CASO INTEGRADOR CON AIRFLOW

> *"Airflow no procesa datos; Airflow procesa tareas. Es el director de la orquesta que decide cuándo entra cada músico."*

### 🏗️ La Evolución del Pipeline

Hasta la sesión pasada, teníamos scripts sueltos y un `correr.py`. Ahora, todo ese trabajo se centraliza en un **DAG de Airflow** (el `tienda_diaria`).

*   **BRONZE:** Múltiples carpetas de carga diarias.
*   **AIRFLOW (Centro):** Se ejecuta todos los días a las **06:00 AM (hora CDMX)**. Toma una fecha de carga y la procesa de principio a fin.
*   **SALIDAS:** `lakehouse/corte=ds/` (la partición de Silver/Gold de ese día) y `vigente.txt` (el puntero).

### 🕸️ La Anatomía del DAG `tienda_diaria`

1.  **Fase de Revisión (Fan-out):** `revisar_pedidos_web`, `revisar_pedidos_tienda`, `revisar_clientes`, `revisar_tipo_cambio` corren **en paralelo**.
2.  **Fase de Transformación (Fan-in):** `transformar` (dbt) espera a que las 4 revisiones terminen con éxito.
3.  **Fase de Publicación:** `publicar` actualiza el puntero `vigente.txt` para que el tablero apunte a la nueva carpeta.

> 💡 **Clave:** Airflow procesa "un día a la vez" usando el parámetro `ds`. Esto es lo que permite hacer backfills (reprocesar el 22/09 si falló) sin tocar el 23/09.

---

## 2. CRON VS. ORQUESTADOR

> *"cron corre comandos; un orquestador corre pipelines."*

El clásico comando de Linux `0 6 * * * python -m transformacion.pipeline` es "ciego". Un orquestador resuelve lo que `cron` no puede:

| ❌ Pregunta sin respuesta en `cron` | ✅ Solución con Airflow |
|--------------------------------------|-------------------------|
| **¿Y si la carga no llegó?** | **Dependencias:** Si falla la revisión, no transforma. |
| **¿Y si falló ayer?** | **Reintentos:** Airflow vuelve a intentar automáticamente. |
| **¿Cómo reproceso la semana?** | **Backfill:** Reprocesa un rango de fechas con un clic. |
| **¿Quién se enteró?** | **Historial y logs:** Todo queda en la UI web con alertas. |

---

## 3. QUÉ HACE Y QUÉ NO HACE AIRFLOW

| ✅ **SÍ hace** | ❌ **NO hace** |
|----------------|----------------|
| Decide **cuándo** corre cada tarea y en qué orden. | **No procesa datos:** eso lo hace Polars, dbt, Spark. |
| Reintenta, registra estados y guarda los logs. | No es una herramienta de **streaming** (Capítulo 4). |
| Recupera días perdidos (catchup) y reprocesa rangos (backfill). | No mueve datos pesados: por XCom solo viajan cosas chicas. |
| Da una UI para ver, pausar y relanzar. | — |

> 💡 **Clave:** XCom (Cross-Communication) es el mecanismo para pasar datos entre tareas. Si la tarea A descarga un DataFrame, no lo pasa por XCom; lo guarda en un Parquet y le pasa a la tarea B solo la **ruta** del archivo.

---

## 4. ARQUITECTURA DE AIRFLOW 3

> *"En Airflow 3 las tareas ya no tocan la base: hablan con el API server"*

El gran cambio de Airflow 3 es el **aislamiento de seguridad**. Los workers ya no pueden importar `Session` de SQLAlchemy para escribir en la BD.

| Aspecto | Airflow 2 | **Airflow 3** |
|---------|-----------|---------------|
| **Acceso a la BD** | Todos los componentes accedían directo. | Solo el **API Server** accede a la BD. |
| **Workers** | Escribían directo en la BD. | Usan el **Task Execution API** (HTTP). |
| **UI y API** | Eran procesos separados. | Unificados en el **API Server** (React + REST). |
| **Parseo de DAGs** | Dentro del Scheduler. | **DAG Processor** independiente. |

> 💡 **Clave:** Si un worker es comprometido, el atacante no puede borrar la base de datos de Airflow. Solo puede reportar el estado de su tarea a través del API Server.

---

## 5. LOS COMPONENTES DE AIRFLOW 3

| Componente | Función |
|------------|---------|
| **DAG Processor** | Lee los archivos `.py` y los serializa en la base de datos. |
| **Scheduler** | Decide qué tarea se ejecuta y cuándo, respetando dependencias. |
| **Executor / Workers** | Ejecutan el código real (Python, dbt, Bash). |
| **Triggerer** | Maneja esperas largas (tareas diferidas) sin ocupar un worker. |
| **API Server** | Puerta única (UI + REST). Los workers le reportan a él, y él escribe en la BD. |
| **Metadata DB** | SQLite (local) o Postgres (producción). Guarda estados, DAGs, XComs. |

> 💡 **Clave:** El modo `airflow standalone` levanta todos los componentes en un solo proceso. Es ideal para el laboratorio y pruebas locales, pero en producción se separan.

---

## 6. EL DAG MÍNIMO

Para que Airflow reconozca un pipeline, se necesita un archivo `.py` con:

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="dag_minimo_moderno",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False
)
def mi_pipeline_minimo():

    @task
    def imprimir_hola():
        print("Hola desde Airflow")

    imprimir_hola()

mi_pipeline_minimo()
```

| Elemento | Obligatorio | Propósito |
|----------|-------------|-----------|
| `dag_id` | Sí | Nombre único en la UI. |
| `start_date` | Sí | Punto de partida del calendario. |
| `schedule` | Sí | Frecuencia (cron o `@daily`). |
| `catchup=False` | Recomendado | Evita ejecuciones masivas del pasado. |
| `@task` | Sí | Define la acción real a ejecutar. |

---

## 7. XCOM: LA REGLA DE ORO

> *"XCom es el mecanismo de Airflow para pasar datos entre tareas. Pero no es un camión de carga, es un mensajero en moto."*

| ✅ **SÍ** (Metadatos pequeños, unos KB) | ❌ **NO** (Datos masivos) |
|------------------------------------------|---------------------------|
| Un conteo (`15000`) | Un DataFrame de 30,000 pedidos. |
| Una ruta de archivo (`s3://bucket/datos.parquet`) | Un JSON gigante con todo el catálogo. |
| Un ID de lote (`lote_2026-11-12`) | Una lista con miles de registros. |

**El Patrón Correcto (Como lo hace `tienda_diaria`):**
1.  La tarea `transformar` escribe la tabla final en `lakehouse/corte=ds/`.
2.  Devuelve por XCom solo el string `"lakehouse/corte=2026-11-12/"`. (Unos cuantos bytes).
3.  La tarea `publicar` recibe el XCom y va a leer el archivo a esa ruta.

> ⚠️ **Apunte clave:** Nunca pases un DataFrame por XCom. Airflow lo serializa y lo guarda en su base de datos, lo que la vuelve lenta o la colapsa.

---

## 8. LOS ESTADOS DE UNA TAREA

> *"En la UI, la vista Grid pinta un cuadro por tarea y por corrida con estos colores: es la primera pantalla que se revisa en la mañana."*

| Estado | Color en UI | ¿Qué significa? |
|--------|-------------|-----------------|
| **`none`** | ⚪ (Gris claro) | La tarea aún no ha sido programada. |
| **`scheduled`** | 🔵 (Azul) | El Scheduler ya determinó que debe correr. |
| **`queued`** | 🔵 (Azul) | Está en la cola del Executor esperando un Worker. |
| **`running`** | 🟡 (Amarillo) | Un Worker la tomó y la está ejecutando. |
| **`success`** | 🟢 (Verde) | Terminó sin errores. |
| **`failed`** | 🔴 (Rojo) | Lanzó una excepción. **Requiere atención.** |
| **`up_for_retry`** | 🟠 (Naranja) | Falló, pero Airflow tiene reintentos automáticos. |
| **`upstream_failed`** | 🟥 (Rojo oscuro) | No corrió porque una tarea anterior falló (Fail-Fast). |
| **`skipped`** | 🩷 (Rosa/Gris) | No corrió porque se decidió saltarla (lógica). |

---

## 9. LA FECHA LÓGICA: ¿QUÉ FECHA "ES" CADA CORRIDA?

> *"En las dos versiones, `ds` es la fecha que la tarea debe procesar. Lo que cambia es cuándo se dispara esa tarea."*

Este es el concepto más confuso de Airflow. El parámetro `ds` (fecha lógica) representa la fecha de los **datos**, no del reloj.

| Versión | Concepto | ¿Cuándo se dispara? | ¿Qué procesa (`ds`)? |
|---------|----------|---------------------|----------------------|
| **Airflow 3** (Actual) | **Disparo (`run_after`)** | Se dispara **al inicio** del día (ej. 08/09 a las 06:00). | Procesa los datos de **ese mismo día** (08/09). |
| **Airflow 2** (Legacy) | **Intervalo** | Se dispara **al final** del intervalo (09/09 a las 06:00). | Procesa los datos del **día anterior** (08/09). |

> 💡 **Clave:** Nunca uses `datetime.now()` en un DAG para filtrar datos. Usa siempre el parámetro `ds` (ej. `WHERE fecha = '{{ ds }}'`). Si usas la fecha del sistema, al hacer backfill procesarás los datos de hoy múltiples veces, rompiendo la idempotencia.

---

## 10. RESUMEN GENERAL DEL CURSO

### 🎓 El Viaje Completo de la Certificación

Hemos recorrido el ciclo de vida completo de la ingeniería de datos (Reis & Housley):

1.  **Sesión 1.1 (Fundamentos):** Arquitectura Medallion (Bronze/Silver/Gold), buenas prácticas (Idempotencia, Atomicidad, etc.) y el ciclo de vida.
2.  **Sesión 1.2 (Ingesta):** Landing zone, metadatos, contratos, APIs (paginación/rate limit), backoff y mojibake.
3.  **Sesión 1.3 (Calidad):** DAMA, contratos de Silver con Pandera, funciones puras y cuarentena.
4.  **Sesión 1.4 (Transformación):** ELT con dbt y DuckDB. SQL para deduplicar y ASOF JOIN. Pruebas (Genéricas, Singulares, Unitarias) y Fail-Fast.
5.  **Sesión 1.5 (Orquestación):** Airflow 3. DAGs, dependencias, XCom (regla de oro) y la fecha lógica (`ds`).

### 📌 Las Reglas de Oro del Ingeniero de Datos

> 1. **"Un pipeline de producción es idempotente, reprocesable, atómico, observable, probado y seguro."**
> 2. **"Lee el CSV como si fuera hostil. Nunca confíes en el encoding por defecto."**
> 3. **"Si un secreto llegó a Git, ya se filtró: rótalo."**
> 4. **"La cuarentena aparta las filas malas; no las borra."**
> 5. **"El núcleo del pipeline debe ser puro (DataFrame -> DataFrame). La suciedad se maneja en las orillas."**
> 6. **"En dbt, si un test falla, protege la capa Gold (Fail-Fast)."**
> 7. **"En Airflow, XCom es para mensajes, no para datos. Pasa la llave, no el tesoro."**
> 8. **"Nunca uses `datetime.now()` en Airflow. La fecha lógica (`ds`) es la que manda."**

### 🎯 Próximos Pasos

*   **El Proyecto Final:** Arrancó en la sesión 1.4. Consiste en demostrar todo el pipeline: ingesta (Python), transformación (dbt) y orquestación (Airflow) sobre el caso de la tienda en línea.
*   **Capítulos futuros (si el curso continúa):** Spark (3.3), Observabilidad (4.3), Despliegue en GCP/AWS (4.2) y Streaming (Capítulo 4).

---

**Nota final:** *"Un pipeline no es un script que corre una vez; es un sistema vivo que se orquesta, se monitorea y se recupera solo. Con dbt y Airflow, dejas de ser un programador que mueve datos, y te conviertes en un ingeniero que diseña sistemas de datos."*

---