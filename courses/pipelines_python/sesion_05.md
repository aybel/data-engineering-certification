# 📓 WORKBOOK - SESIÓN 1.4
## Transformación con dbt, DuckDB y Arquitectura ELT - Pipelines y ETL con Python

**Curso:** Pipelines y ETL con Python | BSG Institute
**Fecha:** 12/11/2026
**Duración:** [pendiente] (Sesión 4 de 14)

---

## 📌 ÍNDICE

1. [Panorama de la Sesión: ¿Dónde estamos?](#1-panorama-de-la-sesión-dónde-estamos)
2. [ETL vs. ELT: Dos Formas de Llegar a Gold](#2-etl-vs-elt-dos-formas-de-llegar-a-gold)
3. [¿Qué es dbt (y qué no es)?](#3-qué-es-dbt-y-qué-no-es)
4. [Anatomía de un Proyecto dbt](#4-anatomía-de-un-proyecto-dbt)
5. [El Grafo (DAG): Orden y Linaje desde el Código](#5-el-grafo-dag-orden-y-linaje-desde-el-código)
6. [SQL que Ya Conocen, con Otra Cara](#6-sql-que-ya-conocen-con-otra-cara)
7. [Tres Tipos de Prueba en dbt](#7-tres-tipos-de-prueba-en-dbt)
8. [dbt build con un Lote Roto (Fail-Fast)](#8-dbt-build-con-un-lote-roto-fail-fast)
9. [Fuentes Externas: Bronze sin Copiar](#9-fuentes-externas-bronze-sin-copiar)
10. [El Mismo Proyecto sobre BigQuery](#10-el-mismo-proyecto-sobre-bigquery)
11. [Laboratorio 2.3: ELT con dbt en Colab](#11-laboratorio-23-elt-con-dbt-en-colab)
12. [¿Siempre se usa esta Arquitectura de Archivos?](#12-siempre-se-usa-esta-arquitectura-de-archivos)
13. [¿Se Pueden Agregar Índices en dbt?](#13-se-pueden-agregar-índices-en-dbt)
14. [Resumen de la Sesión](#14-resumen-de-la-sesión)

---

## 1. PANORAMA DE LA SESIÓN: ¿DÓNDE ESTAMOS?

> *"dbt compila SQL, lo ordena por `ref()`, lo prueba y documenta el linaje."*

### 🏗️ El Mapa del Pipeline Actual

| Capa | Herramienta | Qué contiene |
|------|-------------|--------------|
| **🥉 Bronze** | Parquet (en la Landing) | `pedidos_web`, `pedidos_tienda`, `clientes`, `tipo_cambio` |
| **⚙️ Transformación** | **DuckDB + dbt** | Staging, Intermediate, Marts, Seeds, Snapshots, Pruebas |
| **📊 Consumidores** | **Streamlit** | Tablero |
| **🎓 Proyecto Final** | [Pendiente] | Arranca hoy |

> 💡 **Clave:** Entramos a la fase de **Transformación**. La ingesta ya está resuelta; ahora toca convertir los datos crudos en tablas listas para el negocio (Gold).

---

## 2. ETL VS. ELT: DOS FORMAS DE LLEGAR A GOLD

> *"Lo que cambia es dónde corre el cómputo y quién lo mantiene."*

| Característica | ETL (Extract, Transform, Load) | ELT (Extract, Load, Transform) |
|----------------|--------------------------------|--------------------------------|
| **Orden** | Extraer → **Transformar** → Cargar | Extraer → Cargar → **Transformar** |
| **¿Dónde se transforma?** | Fuera del destino (Python, Spark, Polars) | Dentro del motor analítico (SQL) |
| **Herramienta principal** | Python (Polars, pandas), Spark | SQL (dbt), DuckDB, BigQuery |
| **Sesiones del curso** | 2.1 y 2.2 | **Hoy** (Sesión actual) |

> 💡 **Clave:** ELT es el estándar moderno. Los motores actuales son tan potentes que es más barato cargar todo crudo y dejar que el motor haga el trabajo pesado con SQL.

---

## 3. ¿QUÉ ES DBT (Y QUÉ NO ES)?

> *"dbt no es un orquestador ni una herramienta de ingesta. Es el motor que compila tu SQL y lo convierte en tablas y vistas, con pruebas y documentación incluidas."*

### ✅ Lo que SÍ hace dbt
*   **Compila SELECTs con Jinja:** Escribe SQL dinámico y lo materializa como vistas o tablas.
*   **Ordena la ejecución:** Usa `ref()` y `source()` para construir un grafo (DAG).
*   **Corre pruebas:** Ejecuta tests de calidad en SQL.
*   **Genera documentación y linaje:** Crea automáticamente un sitio web con el mapa de datos.
*   **Es agnóstico al motor:** Funciona sobre DuckDB, BigQuery, Snowflake, Redshift, etc.

### ❌ Lo que NO hace dbt
*   **No extrae:** La ingesta es responsabilidad de Python (Sesiones 1.2 y 1.3).
*   **No orquesta:** La ejecución programada la hace **Airflow** (Capítulo 3).
*   **No mueve datos entre sistemas:** Todo corre en un mismo motor.

> 💡 **Clave:** dbt asume que los datos ya están dentro del motor. Su trabajo empieza con un `SELECT` y termina con una tabla/vista creada.

---

## 4. ANATOMÍA DE UN PROYECTO DBT

> *"dbt no es un script suelto; es un proyecto de software con carpetas, configuraciones, pruebas y un orden de ejecución definido."*

### 📁 Estructura de Directorios

| Carpeta / Archivo | Propósito | Capa Medallion |
|-------------------|-----------|----------------|
| **`dbt_project.yml`** | Configura el proyecto y cómo se materializa cada carpeta. | — |
| **`profiles.yml`** | Configura la conexión al motor (credenciales, ruta). | — |
| **`seeds/`** | Archivos CSV que se cargan como tablas (catálogos). | Catálogos |
| **`models/staging/`** | Limpieza básica. Se materializa como **VISTA**. | Silver |
| **`models/intermediate/`** | Joins, reglas de negocio, deduplicación. **TABLA**. | Silver |
| **`models/marts/`** | Dimensiones y hechos. **TABLA**. | **Gold** |
| **`snapshots/`** | Guarda el histórico de cambios (SCD Tipo 2). | — |
| **`tests/`** | Pruebas de calidad en SQL. | — |
| **`correr.py`** | Script orquestador local (seeds + historia + dbt build). | — |

### 🛠️ Los Comandos que Más Vas a Usar

| Comando | Qué hace |
|---------|----------|
| **`dbt seed`** | Carga los archivos CSV de `seeds/` a la base de datos. |
| **`dbt build`** | Corre modelos, snapshots y pruebas en el orden correcto (DAG). |
| **`dbt build --select +mart_ventas_diarias`** | Corre un modelo y todo lo que necesita (dependencias). |
| **`dbt test --select test_type:unit`** | Corre solo las pruebas unitarias. |
| **`dbt docs generate`** | Genera la documentación y el linaje navegable. |

---

## 5. EL GRAFO (DAG): ORDEN Y LINAJE DESDE EL CÓDIGO

> *"No tienes que decirle a dbt en qué orden correr las cosas. Él lee tu código, conecta las flechas y deduce el orden y el linaje por ti."*

### 🗺️ Lectura del Grafo (De izquierda a derecha)

1.  **Fuentes y Seeds:** `pedidos_web`, `clientes`, `monedas`.
2.  **Staging (Vistas):** Estandarizan nombres y castean tipos.
3.  **Intermediate (Tablas):**
    *   `int_pedidos_unicos`: Une web y tienda.
    *   **La Bifurcación:** Los datos malos van a `int_pedidos_cuarentena` y los buenos a `int_pedidos_validos`.
    *   `snap_clientes`: Guarda el histórico (SCD2).
    *   `int_pedidos_en_pesos`: Cruza con `tipo_cambio`.
4.  **Marts (Gold):** `mart_ventas_diarias`, `fct_pedidos`, `dim_cliente`.

> 💡 **Clave:** En dbt, el código es la documentación. Si sabes leer los `ref()` de tus archivos SQL, el DAG se dibuja solo.

---

## 6. SQL QUE YA CONOCEN, CON OTRA CARA

> *"dbt no inventa un nuevo lenguaje. Solo toma el SQL que ya sabes y lo convierte en un proyecto versionado."*

### 1️⃣ Deduplicar (usando `QUALIFY`)
```sql
select *
from todos
qualify row_number() over (
    partition by origen, pedido_id
    order by actualizado_en desc,
             _extraido_en desc
) = 1
```
*   Agrupa por llave, ordena por fecha descendente y se queda solo con la fila número 1 (la más reciente).

### 2️⃣ Tipo de cambio `ASOF JOIN`
```sql
select p.*, tc.mxn_por_usd
from pedidos p
asof left join stg_tipo_cambio tc
    on p.fecha_negocio >= tc.fecha
```
*   Busca el registro más cercano hacia atrás en el tiempo. Vital para finanzas (el mismo `merge_asof` de Pandas).

### 📦 El Rol de los `Seeds`
Los catálogos (monedas, ciudades) ya no son diccionarios de Python. Ahora son archivos CSV en `seeds/` que el analista puede editar y recargar con `dbt seed`.

---

## 7. TRES TIPOS DE PRUEBA EN DBT

> *"En dbt, las pruebas no son un extra: son parte del ciclo de vida. Si una prueba falla, el pipeline se detiene."*

| Tipo | ¿Dónde se escribe? | ¿Qué hace? | Ejemplos |
|------|--------------------|------------|----------|
| **1. Genéricas** | En archivos **YAML** | Pruebas estándar preconstruidas. | `unique`, `not_null`, `accepted_values`, `relationships` |
| **2. Singulares** | En archivos **`.sql`** dentro de `tests/` | Si la consulta devuelve filas, la prueba falla. | Reglas de lote, rechazo, mediana por carga. |
| **3. Unitarias** | En archivos **YAML** (`unit_tests:`) | Usan datos simulados (mocks). | Validar lógica compleja sin depender de la BD real. |

**Ejemplo de Prueba Unitaria (El profesor mostró este caso):**
```yaml
unit_tests:
  - name: desempate_por_extraccion
    model: int_pedidos_unicos
    given:
      - input: ref('stg_pedidos_web')
        rows:  # misma hora, distinta extracción
          - {pedido_id: 1, estado: entregado, actualizado_en: "09-13 01:56", _extraido_en: "09-13 09:00"}
          - {pedido_id: 1, estado: cancelado, actualizado_en: "09-13 01:56", _extraido_en: "09-17 11:00"}
    expect:
      rows: [{pedido_id: 1, estado: cancelado}]
```

---

## 8. DBT BUILD CON UN LOTE ROTO (FAIL-FAST)

> *"Si un test crítico falla, dbt no construye lo que depende de él. Es mejor no tener dato que tener dato malo."*

### 🎬 La Secuencia de un Fracaso

| Paso | Modelo | Estado | ¿Por qué? |
|------|--------|--------|-----------|
| 1 | `staging` | 🟢 **ok** | Se construyó bien. |
| 2 | `intermediate` | 🟢 **ok** | Se construyó bien. |
| 3 | `assert_rechazo_por_carga` | 🔴 **falla** | El test detectó que el lote está roto. |
| 4 | `int_pedidos_en_pesos` | ⚪ **se salta** | dbt sabe que depende del paso 3. |
| 5 | `fct_pedidos` | ⚪ **se salta** | Depende del paso 4. |
| 6 | `mart_ventas_diarias` | ⚪ **se salta** | Depende del paso 5. |

### ⚖️ Severidad de las Pruebas: `error` vs `warn`

| Severidad | Qué hace | Cuándo usarla |
|-----------|----------|---------------|
| 🛑 **`error`** | Detiene el pipeline. Los modelos dependientes se saltan (fail-fast). | Para reglas críticas. |
| ⚠️ **`warn`** | Avisa pero deja que el pipeline continúe. | Para anomalías menores (ej. 119 pedidos sin cliente en el CRM). |

> ⚠️ **El peligro de Silver:** El modelo se ejecuta antes que su test, por lo que Silver podría ensuciarse antes de que el test lo detecte. Para evitarlo, se usa el patrón **Write-Audit-Publish** (escribir en temporal, auditar, publicar).

---

## 9. FUENTES EXTERNAS: BRONZE SIN COPIAR

> *"La E y la L ya ocurrieron en la ingesta; aquí solo se declara dónde están."*

En lugar de copiar los datos a DuckDB, dbt declara la ubicación física de los archivos Parquet (la landing zone).

```yaml
sources:
  - name: bronze
    config:
      meta:
        external_location: "read_parquet(
          '{{ var('landing') }}/bronze/{name}/*/*.parquet',
          hive_partitioning = true)"
    tables:
      - name: pedidos_web
      - name: pedidos_tienda
```

| Motor | Equivalente |
|-------|-------------|
| **DuckDB** | `read_parquet` sobre la landing (local) |
| **BigQuery** | Tablas externas o BigLake sobre Cloud Storage |
| **AWS** | Tablas de Athena (Glue Catalog) sobre S3 |

> 💡 **Clave:** "Deja los datos donde están y lleva el cómputo hacia ellos".

---

## 10. EL MISMO PROYECTO SOBRE BIGQUERY

> *"El código de transformación es el mismo. Solo cambia el archivo de conexión y un par de detalles de sintaxis."*

Para migrar de DuckDB a BigQuery, solo cambia `profiles.yml`:
```yaml
tienda:
  target: bigquery
  outputs:
    bigquery:
      type: bigquery
      method: oauth
      project: "{{ env_var('GCP_PROYECTO') }}"
      dataset: tienda
      location: US
```

**Lo que cambia:**
1.  **Funciones propias:** `ASOF JOIN` es nativo en DuckDB, en BigQuery se emula con **macros** de dbt.
2.  **Origen:** Bronze pasa de leer un disco local a Tablas Externas sobre Cloud Storage.
3.  **Costo:** BigQuery cobra por bytes leídos (el sandbox es gratis).

---

## 11. LABORATORIO 2.3: ELT CON DBT EN COLAB

> *"El mismo código que correría en un servidor o en la nube, pero ejecutado en un entorno de notebook para aprender los conceptos."*

### ⚙️ Setup del Entorno
```python
%%capture
!pip -q install -U "dbt-core>=1.10" "dbt-duckdb>=1.9" "polars>=1.10" "pandera[polars]>=0.20" duckdb pyarrow
```

### 💻 El Detalle de Oro: Conexiones en DuckDB
```python
def consulta(sql):
    # Abre y CIERRA la base en cada consulta: si el notebook la deja abierta, dbt no puede escribir en ella.
    with duckdb.connect("elt/tienda.duckdb", read_only=True) as c:
        return c.sql(sql).pl()
```
*   **¿Por qué?** DuckDB es una base de datos embebida (un archivo). Dos procesos no pueden escribir en el mismo archivo al mismo tiempo. La función abre la conexión, lee, y la cierra inmediatamente.

---

## 12. ¿SIEMPRE SE USA ESTA ARQUITECTURA DE ARCHIVOS?

> *"dbt no te obliga a usar esta estructura, pero la comunidad y la industria han adoptado este estándar porque funciona."*

*   **Obligatorio:** `dbt_project.yml`, `profiles.yml` y la carpeta `models/`.
*   **Convención (Medallion en dbt):**
    *   `staging/` (Silver, vistas).
    *   `intermediate/` (Silver, lógica).
    *   `marts/` (Gold, hechos y dimensiones).
*   **Soporte:** `seeds/`, `snapshots/`, `tests/`, `macros/`.

> 💡 **Clave:** Sin leer una sola línea de código, cualquier ingeniero de datos sabe por dónde empieza y por dónde termina el flujo.

---

## 13. ¿SE PUEDEN AGREGAR ÍNDICES EN DBT?

> *"dbt no te obliga a olvidar los índices; te permite declararlos como código. Pero la efectividad y la sintaxis dependen completamente del motor que esté debajo."*

### 🐘 En PostgreSQL (El estándar relacional)
Sí se configuran (usando `indexes=[...]` dentro de `{{ config(...) }}`). Aceleran los `JOIN` y los `WHERE` en tablas grandes.

### 🦆 En DuckDB (El motor del laboratorio)
Aquí es diferente. DuckDB está diseñado para analítica (OLAP), no para búsquedas puntuales (OLTP).
*   **Índices automáticos (Zonemap):** DuckDB **crea automáticamente** un índice "Min-Max" en todas las columnas. No tienes que hacer nada. Si consultas `WHERE fecha = '2026-10-01'`, usa ese índice invisible.
*   **Índices ART (Manuales):** Solo sirven para consultas puntuales muy específicas (ej. `WHERE id = 123`). **No aceleran los JOIN ni las agregaciones**.
*   **Costo:** Crear un índice ART **ralentiza mucho las escrituras**. Como en ELT escribimos tablas completas cada vez, tener índices ART puede hacer que tu `dbt build` tarde mucho más.

| Aspecto | PostgreSQL (OLTP) | DuckDB (OLAP / Laboratorio) |
|---------|-------------------|-----------------------------|
| **¿Se configuran en dbt?** | Sí, con `indexes=[...]` | Sí, pero rara vez se usan |
| **Índices automáticos** | No (tú los creas) | **Sí (Zonemap en todas las columnas)** |
| **¿Aceleran JOINs?** | Sí | **No** |
| **Costo en escritura** | Medio | **Alto** (mejor evitarlos) |

> 💡 **Clave:** En DuckDB, la optimización real está en el **particionamiento** y el **formato columnar (Parquet)**, no en los índices tradicionales.

---

## 14. RESUMEN DE LA SESIÓN

### 📌 Lecciones Aprendidas

1. **ETL vs. ELT:** ELT carga el dato crudo al motor y transforma con SQL. dbt es el rey de la "T".
2. **dbt no es mágico:** No extrae ni orquesta. Compila SQL, ordena ejecución (`ref()`), prueba y documenta.
3. **Anatomía:** `staging` (vistas), `intermediate` (lógica), `marts` (Gold).
4. **Grafo (DAG):** Se genera solo. Muestra el orden y el linaje. Si algo falla, protege la capa Gold (Fail-Fast).
5. **Pruebas:** Genéricas (YAML), Singulares (SQL) y Unitarias (mocks). `warn` vs `error`.
6. **Fuentes Externas:** dbt puede leer Parquet sin copiarlo a una tabla (Bronze sin copiar).
7. **Portabilidad:** El mismo proyecto corre en DuckDB y BigQuery cambiando `profiles.yml`.
8. **Índices en DuckDB:** No son necesarios. DuckDB usa Zonemap automático. Los índices ART ralentizan las escrituras.

### 🗂️ Estructura Conceptual del Proyecto

```
📁 elt/ (Proyecto dbt)
├── dbt_project.yml    (Configuración)
├── profiles.yml       (Conexión a DuckDB/BigQuery)
├── seeds/             (Catálogos CSV)
├── models/
│   ├── staging/       (Silver: vistas)
│   ├── intermediate/  (Silver: tablas, lógica)
│   └── marts/         (Gold: tablas, hechos y dims)
├── snapshots/         (Histórico SCD2)
└── tests/             (Calidad de datos)
```

### 🎯 Preparado para la Próxima Sesión

- ✅ Concepto ELT y dbt entendido
- ✅ Anatomía y DAG comprendidos
- ✅ SQL para deduplicar y ASOF JOIN documentado
- ✅ Pruebas y Fail-Fast entendidos
- ✅ Fuentes externas y portabilidad a la nube
- ✅ Laboratorio en Colab ejecutado
- ⏳ Pendiente: Orquestación con Airflow (Capítulo 3)

---

**Nota final:** *"dbt no reemplaza al ingeniero de datos; reemplaza el SQL suelto y desordenado por un proyecto de software versionado, probado y documentado. La transformación corre donde ya viven los datos."*

---