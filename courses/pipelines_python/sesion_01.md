# 📓 WORKBOOK - SESIÓN 1.1
## Lineamientos Generales, Marco de Referencia y Caso Integrador - Pipelines y ETL con Python

**Curso:** Pipelines y ETL con Python | BSG Institute
**Fecha:** 29/09/2026
**Duración:** [pendiente] (Sesión 1 de 14)

---

## 📌 ÍNDICE

1. [Panorama General del Curso](#1-panorama-general-del-curso)
2. [¿Qué es un Pipeline de Datos?](#2-qué-es-un-pipeline-de-datos)
3. [Marco de Referencia: El Ciclo de Vida de la Ingeniería de Datos](#3-marco-de-referencia-el-ciclo-de-vida-de-la-ingeniería-de-datos)
4. [Caso Integrador: La Analítica de una Tienda en Línea](#4-caso-integrador-la-analítica-de-una-tienda-en-línea)
5. [Arquitectura Medallion (Arquitectura de Medallas)](#5-arquitectura-medallion-arquitectura-de-medallas)
6. [Buenas Prácticas de un Pipeline de Producción](#6-buenas-prácticas-de-un-pipeline-de-producción)
7. [¿Cómo Escala un Pipeline?](#7-cómo-escala-un-pipeline)
8. [Fuentes de Datos del Caso](#8-fuentes-de-datos-del-caso)
9. [Salidas del Pipeline: Tablero y ML/IA](#9-salidas-del-pipeline-tablero-y-mlia)
10. [Orquestación, Observabilidad y Despliegue](#10-orquestación-observabilidad-y-despliegue)
11. [Ficha de 6 Puntos: Pipeline de Datos](#11-ficha-de-6-puntos-pipeline-de-datos)
12. [Mapa de Sesiones (14 Sesiones = 1 Pipeline)](#12-mapa-de-sesiones-14-sesiones--1-pipeline)
13. [Relación con los Cursos Anteriores](#13-relación-con-los-cursos-anteriores)
14. [Resumen de la Sesión](#14-resumen-de-la-sesión)

---

## 1. PANORAMA GENERAL DEL CURSO

### 🎯 Idea Central

> *"Un solo pipeline, catorce sesiones."*

El curso no se organiza por temas aislados, sino como la **construcción progresiva de un solo pipeline de datos**. Cada sesión agrega una pieza al caso integrador, de modo que al final del curso el estudiante tiene un pipeline completo funcionando de punta a punta.

### 📊 Enfoque del Curso

| Aspecto | Descripción |
|---------|-------------|
| **Caso integrador** | La analítica de una **tienda en línea** |
| **Duración** | 14 sesiones |
| **Filosofía** | Cada sesión construye una pieza del mismo pipeline |
| **Resultado final** | Un pipeline orquestado, observable y desplegado |

> 💡 **Clave:** A diferencia de otros cursos donde cada tema es independiente, aquí **todo converge en un mismo flujo de datos**. Esto obliga a pensar como ingeniero de datos, no como usuario de herramientas sueltas.

---

## 2. ¿QUÉ ES UN PIPELINE DE DATOS?

> *"Un pipeline de datos es una serie de pasos automatizados por los que pasa el dato desde su origen hasta su destino, transformándose en el camino."*

### 📖 Definición Simple

Un **pipeline de datos** (tubería de datos) es un **conjunto de procesos conectados en secuencia** que mueven datos desde una o varias **fuentes** hasta uno o varios **destinos**, aplicando **transformaciones** en el trayecto, de forma **automatizada y repetible**.

### 🚰 Analogía de la Tubería

> *"Imagina una tubería de agua: el agua entra por un extremo (la fuente), pasa por filtros y válvulas (las transformaciones), y sale por el otro extremo ya lista para consumir (el destino). Un pipeline de datos hace lo mismo, pero con datos."*

```
FUENTE  →  [ transformación ]  →  [ transformación ]  →  DESTINO
   │              │                      │                 │
PostgreSQL    Limpieza              Agregación         Tablero
API REST      Tipado                Modelado           ML/IA
CSV           Validación           Cálculo            Data Warehouse
Eventos       Deduplicación        Métricas
```

### 🔑 Componentes de un Pipeline

| Componente | Pregunta que responde | Ejemplo en el caso integrador |
|------------|----------------------|-------------------------------|
| **Fuente (Source)** | ¿De dónde vienen los datos? | PostgreSQL, API REST, CSV, Eventos |
| **Ingesta** | ¿Cómo los traigo? | Conexión a BD, consumo de API, lectura de archivos |
| **Transformación** | ¿Qué les hago? | Limpieza, tipado, validación, agregación |
| **Destino (Sink)** | ¿A dónde van? | Capa Gold, tablero, modelo ML |
| **Orquestación** | ¿Quién y cuándo los mueve? | Airflow |
| **Observabilidad** | ¿Cómo sé que funcionó? | Logs, alertas, monitoreo |

### 🎯 Características que Definen un Pipeline

| Característica | Descripción |
|----------------|-------------|
| **Automatizado** | No requiere intervención manual cada vez que corre |
| **Repetible** | Se puede ejecutar una y otra vez con el mismo resultado |
| **Programado o por evento** | Corre en un horario fijo o cuando ocurre algo |
| **Trazable** | Se puede saber qué pasó en cada paso |
| **Recuperable** | Si falla, se puede reintentar o reprocesar |

### 🔄 Pipeline vs. Script Suelto

| Script suelto | Pipeline de datos |
|---------------|-------------------|
| Se ejecuta a mano | Se ejecuta solo (programado o por evento) |
| Nadie sabe si falló | Tiene monitoreo y alertas |
| Difícil de repetir | Repetible y reproducible |
| Un solo paso | Múltiples pasos encadenados |
| No escala | Diseñado para crecer |

> 💡 **Clave:** Un script que corre una vez no es un pipeline. Un pipeline es un **sistema de producción** que mueve datos de forma confiable, repetida y observable.

### 🧩 ETL vs. ELT vs. Pipeline

| Concepto | Qué significa | Relación con el pipeline |
|----------|---------------|--------------------------|
| **ETL** | Extract → Transform → Load | Un *tipo* de pipeline: transforma antes de cargar |
| **ELT** | Extract → Load → Transform | Otro *tipo*: carga primero y transforma después (en el destino) |
| **Pipeline** | Término general | El *paraguas* que incluye ETL, ELT y más |

> 💡 **En palabras simples:** Un pipeline es el concepto amplio; ETL y ELT son formas específicas de construirlo. En este curso verás ambos (sesión 2.1 y 2.2).

---

## 3. MARCO DE REFERENCIA: EL CICLO DE VIDA DE LA INGENIERÍA DE DATOS

> *"Basado en Reis y Housley, Fundamentals of Data Engineering (O'Reilly, 2022)."*

### 📖 ¿Qué es el Ciclo de Vida de la Ingeniería de Datos?

Es el **modelo mental** que describe todas las etapas por las que pasa el dato, desde que se genera en un sistema fuente hasta que se consume en analítica, machine learning o ETL inverso. Es el marco que da contexto a **todo el pipeline** que construirás en el curso.

### 🔄 Las Tres Grandes Etapas del Ciclo

```
GENERACIÓN  →  INGESTA  →  TRANSFORMACIÓN  →  SERVICIO  →  CONSUMIDORES
(sistemas       (traer         (limpiar,          (entregar      (analítica,
 fuente)         datos)         modelar)           datos)         ML, ETL inverso)
```

| Etapa | Pregunta que responde | En el caso integrador |
|-------|----------------------|-----------------------|
| **1. Generación** | ¿De dónde nace el dato? | PostgreSQL, API REST, CSV, eventos de clics |
| **2. Ingesta** | ¿Cómo lo traigo? | Conectores a BD, consumo de API, lectura de archivos |
| **3. Transformación** | ¿Qué le hago? | Limpieza, tipado, validación, agregación (Bronze→Silver→Gold) |
| **4. Servicio** | ¿Cómo lo entrego? | Tablero, API de datos, tablas Gold |
| **5. Consumidores** | ¿Quién lo usa? | Analítica, ML/IA, ETL inverso |

### 💾 Almacenamiento (Atraviesa Todas las Etapas)

> *"El almacenamiento no es una etapa: es una capa transversal que sostiene todo el ciclo."*

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | El lugar donde el dato vive entre cada etapa |
| **Ejemplos** | Data lake (S3, GCS), data warehouse (BigQuery, Redshift), BD operacional |
| **En el curso** | Las capas Bronze, Silver y Gold del patrón Medallion |
| **Por qué es transversal** | Cada etapa lee de un almacenamiento y escribe en otro |

> 💡 **Clave:** Sin almacenamiento, cada etapa tendría que pasar el dato directamente a la siguiente en memoria. El almacenamiento permite **desacoplar** las etapas y **reprocesar**.

### 🎯 Los Tres Consumidores Finales

| Consumidor | Qué hace | Sesión del curso |
|------------|----------|------------------|
| **📊 Analítica** | Reportes, dashboards, KPIs de negocio | 2.2 (Tablero) |
| **🤖 Machine Learning** | Modelos predictivos sobre datos curados | 4.3 (ML/IA) |
| **🔄 ETL inverso** | Devolver datos procesados a los sistemas operativos (ej. recomendaciones en la app) | [pendiente] |

> 💡 **Clave:** El **ETL inverso** (reverse ETL) es el más olvidado: lleva el dato **de vuelta** desde Gold hacia los sistemas operativos (CRM, app, marketing). Cierra el ciclo.

### 🌊 Las Corrientes de Fondo (Undercurrents)

> *"No son etapas del ciclo: son disciplinas que atraviesan TODAS las etapas."*

| Corriente | Qué aporta | Ejemplo en el caso |
|-----------|------------|--------------------|
| **🔒 Seguridad** | Proteger el dato en todo momento | Cifrado, control de acceso, PII |
| **📋 Gestión de datos** | Gobernanza, catálogo, linaje | Saber de dónde viene cada dato |
| **⚙️ DataOps** | Automatización, CI/CD, monitoreo | Pipelines reproducibles y observables |
| **🏗️ Arquitectura** | Diseño del sistema | Medallion, elección de motores |
| **🎛️ Orquestación** | Coordinar tareas | Airflow (sesiones 3.1, 3.2) |
| **💻 Ingeniería de software** | Buenas prácticas de código | Testing, modularidad, versionado |

> 💡 **Clave:** Las corrientes de fondo son lo que **distingue a un ingeniero de datos de un analista que escribe scripts**. No basta con mover datos: hay que hacerlo con seguridad, gobernanza, automatización y buen código.

### 🧩 Cómo Encaja Este Marco con el Caso Integrador

```
GENERACIÓN          INGESTA        TRANSFORMACIÓN         SERVICIO        CONSUMIDORES
──────────         ────────        ─────────────         ────────        ────────────
PostgreSQL  ──┐
API REST    ──┼──→  Ingesta  ──→   Bronze→Silver→Gold ──→  Tablas Gold ──→  📊 Tablero
CSV         ──┤      (1.2,1.3)     (2.1, 2.2, 2.3)        (API de datos)     🤖 ML/IA
Eventos     ──┘                                                                   🔄 ETL inverso
              │
              └── ALMACENAMIENTO (Bronze / Silver / Gold) ──────────────────────┘
              └── CORRIENTES: Seguridad · DataOps · Orquestación · Arquitectura ─┘
```

---

## 4. CASO INTEGRADOR: LA ANALÍTICA DE UNA TIENDA EN LÍNEA

El caso simula el flujo de datos real de una tienda en línea, desde las fuentes operativas hasta los consumidores finales (tablero y modelos de ML/IA).

### 🏗️ Flujo General

```
FUENTES  →  INGESTA  →  BRONZE  →  SILVER  →  GOLD  →  CONSUMIDORES
```

### 🎯 Objetivo del Caso

Construir un pipeline que permita responder preguntas de negocio de una tienda en línea, integrando datos de múltiples fuentes en un solo flujo confiable.

### 🗺️ Diagrama del Caso Integrador

| Bloque | Contenido | Sesiones |
|--------|-----------|----------|
| **Fuentes** | PostgreSQL · API REST · CSV · Eventos | — |
| **Ingesta** | Traer datos de las cuatro fuentes | 1.2 · 1.3 · 4.1 |
| **🥉 Bronze** | Datos crudos | 2.1 |
| **🥈 Silver** | Limpios y validados | 2.2 · 2.3 |
| **🥇 Gold** | Listos para consumir | 2.2 |
| **Consumidores** | Tablero · ML/IA | 2.2 · 4.3 |
| **Transversal** | Orquestación Airflow · Observabilidad · Despliegue GCP/AWS | 3.1 · 3.2 · 4.3 · 4.2 |

> 💡 **Clave:** La sesión 3.3 (Spark) aplica transversalmente al procesamiento de las capas.

---

## 5. ARQUITECTURA MEDALLION (ARQUITECTURA DE MEDALLAS)

> *"El profesor la llamó arquitectura Medallion, o arquitectura de medallas."*

### 🏅 ¿Qué es la Arquitectura Medallion?

Es un patrón de diseño de pipelines de datos que organiza la información en **tres capas con niveles crecientes de calidad**, nombradas como las medallas olímpicas:

| Medalla | Capa | Nivel | Qué contiene |
|---------|------|-------|--------------|
| 🥉 **Bronze** | Datos crudos | Bajo | Lo que llega tal cual de las fuentes, sin transformar |
| 🥈 **Silver** | Datos limpios y validados | Medio | Datos tipados, sin duplicados, con reglas de calidad aplicadas |
| 🥇 **Gold** | Datos listos para consumir | Alto | Datos agregados y modelados para negocio |

### 🎯 Idea Central del Patrón

> *"Cada medalla representa un nivel de confianza en el dato. Bronze confía poco, Silver confía más, Gold es el dato en el que el negocio puede basar decisiones."*

### 🔑 Principios de la Arquitectura Medallion

| Principio | Descripción |
|-----------|-------------|
| **Preservación** | Bronze conserva el dato original tal como llegó (trazabilidad) |
| **Refinamiento progresivo** | Cada capa mejora la calidad sin perder la anterior |
| **Separación de responsabilidades** | Ingesta, limpieza y modelado viven en capas distintas |
| **Reprocesabilidad** | Si algo falla en Silver o Gold, se puede reprocesar desde Bronze |
| **Consumo final** | Gold es la única capa que consumen tableros y modelos ML/IA |

### 🔄 Flujo del Dato a Través de las Medallas

```
🥉 Bronze          🥈 Silver           🥇 Gold
(dato crudo)  →   (dato limpio)  →   (dato de negocio)
     │                  │                   │
  Sin tocar       Validado y          Agregado y
  tal como        tipado, sin         modelado para
  llegó           duplicados          tablero / ML
```

### 🧠 Analogía para Recordarla

> *"Bronze es la materia prima que llega al almacén, Silver es el producto ya clasificado y limpio en bodega, y Gold es el producto listo para poner en el anaquel y vender."*

> 💡 **Clave:** La arquitectura Medallion no es exclusiva de este curso: es un estándar de la industria (muy usado en Databricks, Azure y GCP) para organizar lagos de datos. Aprenderla aquí te sirve directamente en el mundo laboral.

### 🔄 Transformación ETL/ELT y Calidad

| Concepto | Sesión | Descripción |
|----------|--------|-------------|
| **ETL/ELT** | 2.1 · 2.2 | Extracción, transformación y carga |
| **Calidad** | 2.3 | Validación y reglas de calidad del dato |
| **Spark** | 3.3 | Procesamiento distribuido para volúmenes grandes |

---

## 6. BUENAS PRÁCTICAS DE UN PIPELINE DE PRODUCCIÓN

> *"Un pipeline de producción no solo mueve datos: los mueve bien. Estas seis propiedades son el estándar mínimo."*

### 📋 Las Seis Buenas Prácticas

| # | Práctica | Pregunta que responde | Riesgo que evita |
|---|----------|----------------------|------------------|
| **1** | 🔁 **Idempotente** | ¿Correrlo varias veces da el mismo resultado? | Duplicar datos |
| **2** | 🔄 **Reprocesable** | ¿Puedo volver a correrlo si algo falla? | Quedarse sin datos |
| **3** | 🧱 **Atómico** | ¿Todo o nada? | Datos a medias |
| **4** | 👁️ **Observable** | ¿Puedo ver qué está pasando? | Fallas silenciosas |
| **5** | 🧪 **Probado** | ¿Sé que funciona antes de producción? | Romper en prod |
| **6** | 🔒 **Seguro** | ¿Los datos están protegidos? | Fugas, accesos indebidos |

> 💡 **Clave:** Estas seis prácticas se complementan. Ninguna sola basta: un pipeline puede ser idempotente pero no observable, o seguro pero no reprocesable.

---

### 🔁 1. IDEMPOTENTE

> *"Correrlo una vez o diez veces produce el mismo resultado."*

| Aspecto | Detalle |
|---------|---------|
| **Qué significa** | Ejecutar el pipeline múltiples veces sobre los mismos datos de entrada da siempre el mismo resultado final |
| **Por qué importa** | Permite reintentos seguros, backfills y reprocesamientos sin duplicar |
| **Cómo se logra** | MERGE/UPSERT, DELETE+INSERT por partición, claves únicas, overwrite |
| **Antipatrón** | `INSERT` ciego que duplica en cada corrida |

#### 🧠 Analogía

> *"Es como un interruptor de luz: no importa cuántas veces lo presiones si ya está encendido, la luz sigue encendida."*

#### 🆚 Pipeline Idempotente vs. No Idempotente

| Escenario | Pipeline NO idempotente | Pipeline idempotente |
|-----------|-------------------------|----------------------|
| Corre 1 vez | 100 registros en Gold | 100 registros en Gold |
| Corre 2 veces | 200 registros (¡duplicados!) | 100 registros (mismo resultado) |
| Corre 3 veces | 300 registros (¡peor!) | 100 registros (mismo resultado) |
| Falla a mitad | Datos inconsistentes | Se reintenta sin problema |

#### 🛠️ Técnicas para Lograr Idempotencia

| Técnica | Cómo ayuda |
|---------|------------|
| **MERGE / UPSERT** | Actualiza si existe, inserta si no existe (no duplica) |
| **DELETE + INSERT por partición** | Borra la partición del día antes de recargarla |
| **Claves únicas** | Restricción que impide insertar duplicados |
| **Escritura por sobrescritura (overwrite)** | Reemplaza el destino en vez de agregar |
| **Idempotency keys** | Identificador único por ejecución/registro |
| **Particionamiento por fecha** | Permite reprocesar solo la partición afectada |

#### 🖼️ Idempotencia en una Imagen (Ejemplo SQL)

**❌ NO IDEMPOTENTE**

```sql
-- Cada corrida agrega otra copia del día
INSERT INTO ventas
SELECT * FROM staging_ventas
WHERE fecha = '2026-09-28';
```

**Problema:** La segunda corrida = **ventas del día duplicadas**.

| Corrida | Registros en `ventas` (fecha 2026-09-28) |
|---------|------------------------------------------|
| 1ª | 1,000 |
| 2ª | 2,000 ⚠️ |
| 3ª | 3,000 ⚠️⚠️ |

**✅ IDEMPOTENTE**

```sql
BEGIN;
DELETE FROM ventas
WHERE fecha = '2026-09-28';

INSERT INTO ventas
SELECT * FROM staging_ventas
WHERE fecha = '2026-09-28';
COMMIT;
```

**Solución:** Reemplaza la partición completa dentro de una transacción.

| Corrida | Registros en `ventas` (fecha 2026-09-28) |
|---------|------------------------------------------|
| 1ª | 1,000 |
| 2ª | 1,000 ✅ |
| 3ª | 1,000 ✅ |

#### 🔍 Doble Lección del Ejemplo

| Práctica | Cómo se aplica en el ejemplo |
|----------|------------------------------|
| 🔁 **Idempotente** | El `DELETE ... WHERE fecha = X` borra la partición antes de recargarla; correrlo N veces da el mismo resultado |
| 🧱 **Atómico** | El `BEGIN ... COMMIT` garantiza que borrado e inserción ocurren como **una sola unidad**: o ambos, o ninguno |

> 💡 **Clave:** Sin la transacción, si el pipeline muere entre el `DELETE` y el `INSERT`, la tabla quedaría **vacía**. Con transacción, se revierte todo y queda intacta.

#### 🔑 El Patrón: "Reemplazar la Partición"

```
1. BEGIN (abrir transacción)
   ↓
2. DELETE de la partición (ej. fecha = '2026-09-28')
   ↓
3. INSERT de los datos nuevos de esa partición
   ↓
4. COMMIT (confirmar todo junto)
```

| Ventaja | Por qué |
|---------|---------|
| **Idempotente** | Correr N veces → mismo resultado |
| **Atómico** | O se reemplaza todo, o no se toca nada |
| **Reprocesable** | Se puede volver a correr la fecha sin miedo |
| **Simple** | Fácil de entender y auditar |
| **Rápido** | Se opera solo sobre una partición, no toda la tabla |

#### 🧩 Variantes del Patrón Según el Motor

| Técnica | Motor típico | Cuándo usarla |
|---------|--------------|---------------|
| `DELETE + INSERT` en transacción | PostgreSQL, SQLite, MySQL | Lo más simple y universal |
| `MERGE` / `UPSERT` | PostgreSQL, BigQuery, Snowflake | Cuando no se quiere borrar todo |
| `INSERT OVERWRITE` | Spark, Hive, BigQuery | Sobrescritura nativa de partición |
| **Swap de tabla** | Cualquiera | Escribir en `ventas_new`, luego `RENAME` |
| **Escritura por overwrite** | dbt, Spark | El modelo recalcula la tabla completa |

#### ⚠️ Antipatrón: `INSERT` Ciego

| Síntoma | Causa |
|---------|-------|
| Ventas que crecen cada día sin explicación | `INSERT` ciego que acumula |
| Métricas infladas | Duplicados por reintentos de Airflow |
| Datos imposibles de reconciliar | Sin control de partición |

**Solución:** siempre preguntarse *"¿qué pasa si este paso corre dos veces?"* antes de escribir un `INSERT`.

#### 🎯 Regla de Oro

> **"Un pipeline de producción debe ser idempotente. Si no lo es, no está listo para producción."**

---

### 🔄 2. REPROCESABLE

> *"Si algo falla o el dato sale mal, puedo volver a correr el pipeline para arreglarlo."*

| Aspecto | Detalle |
|---------|---------|
| **Qué significa** | El pipeline puede volver a ejecutarse para un periodo pasado (backfill) o tras una falla |
| **Por qué importa** | Los pipelines fallan: red, fuente caída, bug en transformación. Hay que poder recuperarse |
| **Cómo se logra** | Datos crudos preservados (Bronze), parámetros de fecha, particionamiento, idempotencia |
| **Diferencia con idempotencia** | Idempotencia = *no duplica*; Reprocesabilidad = *puedo repetir hacia atrás en el tiempo* |

> 💡 **Clave:** La **reprocesabilidad depende del Bronze**: si guardas el dato crudo tal como llegó, siempre puedes reprocesar Silver y Gold.

---

### 🧱 3. ATÓMICO

> *"O se completa todo, o no se completa nada. No hay estados intermedios."*

| Aspecto | Detalle |
|---------|---------|
| **Qué significa** | Cada tarea o transacción del pipeline se ejecuta completa o se revierte por completo |
| **Por qué importa** | Evita datos a medias: si falla a mitad de la carga, no deja Gold inconsistente |
| **Cómo se logra** | Transacciones ACID, `commit`/`rollback`, escritura en staging + swap, operaciones de una sola unidad |
| **Antipatrón** | Insertar 500 de 1000 registros y que el proceso muera dejando la tabla a medias |

> 💡 **Clave:** Este es el mismo principio **ACID** que ya conoces de SQLite y PostgreSQL, aplicado a nivel de pipeline.

---

### 👁️ 4. OBSERVABLE

> *"Puedo ver qué está pasando, cuándo falló y por qué, sin adivinar."*

| Aspecto | Detalle |
|---------|---------|
| **Qué significa** | El pipeline expone su estado interno mediante métricas, logs, trazas y alertas |
| **Por qué importa** | Sin observabilidad, un pipeline es una caja negra: falla y nadie sabe por qué |
| **Cómo se logra** | Métricas, logs estructurados, validaciones de calidad, alertas, dashboards de monitoreo |
| **Antipatrón** | Pipeline que "funciona" pero nadie sabe si corrió, cuánto tardó o si dejó datos malos |

#### 🔭 Los Tres Pilares de la Observabilidad

| Pilar | Pregunta que responde | Ejemplo |
|-------|----------------------|---------|
| **📈 Métricas** | ¿Cuánto, cuántos, cuánto tiempo? | Registros procesados, duración, tasa de error |
| **📝 Logs** | ¿Qué pasó exactamente? | "Ingesta de pedidos iniciada a las 03:00" |
| **✅ Validaciones de calidad** | ¿El dato es confiable? | "0 nulos en columna `monto`" |

> 💡 **Clave:** Los tres se complementan. Las métricas avisan **que** algo pasa, los logs dicen **qué** pasó, y las validaciones confirman **si el dato sirve**.

#### 📈 Métricas

| Tipo de Métrica | Qué mide | Ejemplo en el caso integrador |
|-----------------|----------|-------------------------------|
| **Volumen** | Cuántos registros se procesan | 15,000 pedidos ingestados |
| **Duración** | Cuánto tarda cada etapa | Ingesta: 2 min · Transformación: 5 min |
| **Tasa de error** | % de registros que fallan | 0.3% de pedidos con error |
| **Latencia** | Tiempo desde la fuente hasta Gold | 15 min de extremo a extremo |
| **Frescura (freshness)** | Qué tan reciente es el dato | Gold actualizado hace 10 min |
| **Throughput** | Registros por segundo | 500 reg/s en la ingesta |
| **Costo** | Recursos consumidos | $0.02 por corrida en GCP |

**Herramientas típicas:** Prometheus, Grafana, Cloud Monitoring (GCP), CloudWatch (AWS).

#### 📝 Logs

| Nivel de Log | Cuándo se usa | Ejemplo |
|--------------|---------------|---------|
| **DEBUG** | Detalle fino para depurar | "Leyendo fila 1,234 del CSV" |
| **INFO** | Eventos normales | "Ingesta de pedidos completada: 15,000 registros" |
| **WARNING** | Algo raro pero no crítico | "3 pedidos sin cliente_id, se omiten" |
| **ERROR** | Algo falló | "No se pudo conectar a PostgreSQL" |
| **CRITICAL** | Falla grave que detiene el pipeline | "API REST devolvió 500, abortando" |

**Buenas prácticas de logging:**
- Logs **estructurados** (JSON) para poder consultarlos.
- Incluir **timestamp, etapa, id de ejecución**.
- **No loggear datos sensibles** (tarjetas, contraseñas).
- Centralizar logs (ELK, Cloud Logging, CloudWatch).

#### ✅ Validaciones de Calidad

| Dimensión de calidad | Pregunta | Ejemplo de validación |
|----------------------|----------|----------------------|
| **Completitud** | ¿Faltan datos? | `monto` no puede ser nulo |
| **Unicidad** | ¿Hay duplicados? | `pedido_id` debe ser único |
| **Validez** | ¿El formato es correcto? | `fecha` en formato ISO 8601 |
| **Consistencia** | ¿Concuerda entre tablas? | `cliente_id` existe en clientes |
| **Rango** | ¿Está dentro de lo esperado? | `monto` > 0 y < 1,000,000 |
| **Actualidad** | ¿El dato es reciente? | Gold no puede tener más de 24 h |
| **Exactitud** | ¿Refleja la realidad? | Suma de pedidos = suma de líneas |

**Herramientas típicas:** Great Expectations, dbt tests, Pandera, Soda.

**¿Qué hacer cuando falla una validación?**
1. **Detener** el pipeline (fail-fast) o
2. **Cuarentenar** los registros malos y continuar, o
3. **Alertar** y dejar decidir al humano.

#### 🎯 Las Tres Juntas en el Caso Integrador

```
INGESTA → BRONZE → SILVER → GOLD → TABLERO
   │         │        │       │
   ├─ métricas: cuántos, cuánto tiempo
   ├─ logs: qué pasó en cada paso
   └─ validaciones: ¿el dato cumple las reglas?
```

| Capa | Métrica clave | Log clave | Validación clave |
|------|---------------|-----------|------------------|
| **Ingesta** | Registros traídos | "Conexión OK a PostgreSQL" | Fuente respondió |
| **Bronze** | Registros crudos | "Archivo guardado" | Esquema esperado |
| **Silver** | % válidos | "1,200 registros limpiados" | Sin nulos en claves |
| **Gold** | Métricas de negocio | "Agregación completada" | Sumas cuadran |

---

### 🧪 5. PROBADO

> *"Sé que funciona porque lo probé, no porque tuve suerte."*

| Aspecto | Detalle |
|---------|---------|
| **Qué significa** | El pipeline tiene pruebas automatizadas que verifican su correcto funcionamiento |
| **Por qué importa** | Evita que un cambio rompa algo en producción sin que nadie se dé cuenta |
| **Cómo se logra** | Tests unitarios (funciones), tests de integración (etapas), tests de datos (calidad), CI/CD |

| Tipo de prueba | Qué verifica |
|----------------|--------------|
| **Unitaria** | Que una función haga lo que debe |
| **Integración** | Que las etapas se conecten bien |
| **Regresión** | Que un cambio no rompa lo que ya funcionaba |
| **De datos** | Que el dato cumpla reglas de calidad |

---

### 🔒 6. SEGURO

> *"El dato está protegido en todo momento: en tránsito, en reposo y en acceso."*

| Aspecto | Detalle |
|---------|---------|
| **Qué significa** | El pipeline protege los datos sensibles y controla quién puede verlos o modificarlos |
| **Por qué importa** | Fugas de datos = sanciones legales, pérdida de confianza, daño reputacional |
| **Cómo se logra** | Cifrado, control de acceso (IAM), enmascaramiento de PII, secretos gestionados, auditoría |
| **Antipatrón** | Contraseñas hardcodeadas, datos de tarjetas en logs, accesos abiertos |

| Práctica de seguridad | Aplicación |
|-----------------------|------------|
| **Cifrado en tránsito** | TLS entre pipeline y fuentes |
| **Cifrado en reposo** | Datos cifrados en S3/GCS/BigQuery |
| **Gestión de secretos** | Variables de entorno, Vault, Secret Manager |
| **Enmascaramiento PII** | Ocultar tarjetas, emails, teléfonos |
| **Control de acceso** | Roles mínimos necesarios (least privilege) |
| **Auditoría** | Registro de quién accedió a qué y cuándo |

---

### 🧩 Las Seis Buenas Prácticas y la Arquitectura Medallion

| Capa | Idempotente | Reprocesable | Atómico | Observable | Probado | Seguro |
|------|-------------|--------------|---------|------------|---------|--------|
| 🥉 **Bronze** | Sobrescribe partición | ✅ Dato crudo preservado | Escritura atómica por lote | Log de ingesta | Test de esquema | PII cifrada |
| 🥈 **Silver** | MERGE / upsert | ✅ Reprocesa desde Bronze | Transacción por lote | Métricas de calidad | Tests de datos | Enmascarado |
| 🥇 **Gold** | Recalcula agregados | ✅ Reprocesa desde Silver | Swap de tabla | Frescura y SLA | Tests de negocio | Acceso restringido |

### 📌 Regla de Oro

> **"Un pipeline no es de producción hasta que es idempotente, reprocesable, atómico, observable, probado y seguro. Las seis, no cinco."**

---

## 7. ¿CÓMO ESCALA UN PIPELINE?

> *"Un pipeline que funciona con 1,000 registros no necesariamente funciona con 100 millones. Escalar es diseñarlo para crecer."*

### 🎯 ¿Qué Significa Escalar?

Escalar un pipeline es **aumentar su capacidad** para procesar **más volumen, más velocidad o más variedad** de datos **sin degradar el tiempo ni la calidad**.

### 🔑 Las Tres Dimensiones del Crecimiento

| Dimensión | Qué crece | Reto |
|-----------|-----------|------|
| **Volumen** | Más registros / más GB | Procesar sin morir en memoria |
| **Velocidad** | Más frecuencia / menor latencia | Correr más seguido o en tiempo real |
| **Variedad** | Más fuentes / más formatos | Integrar sin romper el pipeline |

### 🆚 Escalado Vertical vs. Horizontal

| Tipo | Cómo escala | Ventaja | Limitación |
|------|-------------|---------|------------|
| **Vertical (scale up)** | Máquina más grande (más RAM/CPU) | Simple | Tope físico y costo alto |
| **Horizontal (scale out)** | Más máquinas en paralelo | Sin tope práctico | Requiere diseño distribuido |

> 💡 **Clave:** Los pipelines modernos escalan **horizontalmente** (Spark, BigQuery, Databricks). Ese es el motivo por el que el curso incluye **Spark (sesión 3.3)**.

### 🛠️ Estrategias para Escalar un Pipeline

| Estrategia | Cómo ayuda |
|------------|------------|
| **Particionamiento** | Procesar por fecha/región en lugar de todo junto |
| **Paralelización** | Dividir el trabajo en tareas simultáneas |
| **Procesamiento distribuido** | Spark para repartir la carga entre nodos |
| **Procesamiento incremental** | Solo lo nuevo, no todo cada vez |
| **Columnar + compresión** | Leer menos bytes (Parquet, ORC) |
| **Push-down de cómputo** | Que la BD haga el trabajo, no Python |
| **Caché / materialización** | Evitar recalcular lo que no cambió |
| **Auto-scaling** | La nube ajusta recursos según demanda |

### ⚠️ Cuellos de Botella Típicos al Escalar

| Cuello de botella | Síntoma | Solución |
|-------------------|---------|----------|
| **Memoria** | `MemoryError` en pandas | Polars, chunks, Spark |
| **Una sola máquina** | Todo tarda cada vez más | Distribuir con Spark |
| **Escritura concurrente** | Bloqueos en BD | Colas, batch, particiones |
| **Recalcular todo** | Corridas eternas | Procesamiento incremental |
| **Formato ineficiente** | Leer GB cuando bastan MB | Parquet + particionado |

### 🧩 Escalabilidad y Arquitectura Medallion

| Capa | Cómo escala |
|------|-------------|
| 🥉 **Bronze** | Almacenamiento barato (S3/GCS), sin transformar |
| 🥈 **Silver** | Procesamiento distribuido (Spark) e incremental |
| 🥇 **Gold** | Agregaciones precalculadas, columnar, particionado |

### 📌 Reglas de Oro de la Escalabilidad

> 1. **Diseña para crecer desde el día uno** (no cuando ya duele).
> 2. **Procesa incremental**, no todo cada vez.
> 3. **Paraleliza** lo que se pueda partir.
> 4. **Mide** antes de optimizar (métricas).
> 5. **Escala horizontal**, no solo vertical.

### 📝 Aplicado al Caso Integrador

- La tienda en línea empieza con miles de pedidos, pero puede llegar a millones.
- Los **eventos de clics** crecen más rápido que todo lo demás → candidatos a streaming.
- El pipeline debe poder **correr cada hora o cada minuto** sin rehacer todo.
- Gold debe estar **particionado por fecha** para que el tablero consulte rápido.

---

## 8. FUENTES DE DATOS DEL CASO

El pipeline ingesta desde **cuatro fuentes** distintas, lo cual obliga a manejar formatos y conectores heterogéneos.

| Fuente | Contenido | Tipo |
|--------|-----------|------|
| **PostgreSQL** | Pedidos y clientes | Base de datos relacional |
| **API REST** | Catálogo y tipo de cambio | Servicio web |
| **Archivos CSV** | Inventario de proveedores | Archivo plano |
| **Eventos** | Clics en el sitio | Datos de comportamiento / streaming |

> 💡 **Clave:** Cada fuente representa un reto distinto de ingesta: conexión a BD, consumo de API, lectura de archivos y captura de eventos. Esto conecta directamente con lo visto en el curso de Bases de Datos y SQL.

---

## 9. SALIDAS DEL PIPELINE: TABLERO Y ML/IA

Los datos de la capa **Gold** alimentan dos consumidores finales:

| Consumidor | Sesión | Descripción |
|------------|--------|-------------|
| **📊 Tablero** | 2.2 | Visualización de métricas de negocio |
| **🤖 ML / IA** | 4.3 | Modelos de machine learning sobre los datos curados |

> 💡 **Clave:** El pipeline no termina en la capa Gold: termina cuando **alguien consume el dato**. Esto es lo que distingue a un ingeniero de datos de un simple programador.

---

## 10. ORQUESTACIÓN, OBSERVABILIDAD Y DESPLIEGUE

Esta es la capa transversal que sostiene todo el pipeline:

| Componente | Sesión | Función |
|------------|--------|---------|
| **Orquestación con Airflow** | 3.1 · 3.2 | Programar y coordinar las tareas del pipeline |
| **Observabilidad** | 4.3 | Monitoreo, logs y alertas del pipeline |
| **Despliegue en GCP y AWS** | 4.2 | Puesta en producción del pipeline en la nube |

> 💡 **Clave:** Un pipeline que no está orquestado, monitoreado y desplegado **no es un pipeline de producción**, es solo un script.

### 🧩 Idempotencia y Orquestación (Airflow)

> *"Airflow puede reintentar una tarea automáticamente. Pero si la tarea no es idempotente, cada reintento empeora los datos en lugar de arreglarlos."*

| Concepto de Airflow | Relación con idempotencia |
|---------------------|---------------------------|
| **Retries** | Solo son seguros si la tarea es idempotente |
| **Backfill** | Requiere que el pipeline sea idempotente por fecha |
| **Task instance** | Cada ejecución debe dejar el mismo estado final |
| **SLA / alertas** | Monitorean que la corrida idempotente termine bien |

---

## 11. FICHA DE 6 PUNTOS: PIPELINE DE DATOS

> *"Así como en el curso de Bases de Datos fichábamos cada motor, aquí fichamos el concepto central del curso: el pipeline de datos."*

| # | Punto | Pipeline de Datos |
|---|-------|-------------------|
| **1** | **Modelo de datos que asume** | Flujo secuencial de datos entre capas (Bronze → Silver → Gold); no impone un modelo único, sino una **dirección y transformación progresiva** |
| **2** | **Operaciones en las que resulta eficiente** | Ingesta multi-fuente, limpieza, validación, agregación, carga a destinos y alimentación de consumidores (tablero, ML) |
| **3** | **Garantías de consistencia que ofrece** | Depende del diseño: **idempotencia, atomicidad, reprocesabilidad, validaciones de calidad y observabilidad** en cada capa |
| **4** | **Relación entre costo de escritura y costo de lectura** | Costo se concentra en **escritura/transformación** (procesar y mover datos); la lectura es barata porque Gold ya está optimizado para consumo |
| **5** | **Interfaz desde Python** | `pandas` / `polars` para transformar, `sqlite3` / `psycopg2` para BD, `requests` para APIs, `Airflow` para orquestar, `boto3` / SDKs de GCP para desplegar |
| **6** | **Escenario en el que conviene y en el que no** | ✅ **Conviene:** cuando hay datos dispersos, necesidad de automatizar, múltiples consumidores o datos que deben llegar confiables y a tiempo.<br>❌ **No conviene:** cuando el dato se consume una sola vez de forma manual, no cambia con frecuencia, o no requiere transformación ni repetición |

### 💡 Lectura de la Ficha

- **Punto 1:** El pipeline no es un motor de BD, es un **patrón de flujo**.
- **Punto 2:** Su fuerte es **mover y refinar** datos, no almacenarlos como fin.
- **Punto 3:** La confiabilidad no viene del motor sino del **diseño** (idempotencia, atomicidad, validaciones, observabilidad).
- **Punto 4:** El costo real está en **procesar**, no en leer.
- **Punto 5:** Python es el **pegamento** que conecta todas las piezas.
- **Punto 6:** Un pipeline tiene sentido cuando el dato debe **repetirse, automatizarse y confiarse**.

> 🧠 **En palabras simples:** *"Un pipeline conviene cuando el dato tiene que viajar solo, llegar limpio y llegar a tiempo. No conviene cuando basta con abrir un CSV a mano una vez."*

---

## 12. MAPA DE SESIONES (14 SESIONES = 1 PIPELINE)

| Sesión | Tema | Pieza que construye |
|--------|------|---------------------|
| 1.1 | Lineamientos y caso integrador | Panorama general |
| 1.2 | Ingesta | Ingesta de fuentes |
| 1.3 | Ingesta | Ingesta de fuentes |
| 4.1 | Ingesta | Ingesta de fuentes |
| 2.1 | Transformación ETL/ELT | Capa Bronze → Silver |
| 2.2 | Transformación ETL/ELT + Tablero | Silver → Gold + Tablero |
| 2.3 | Calidad del dato | Validaciones en Silver |
| 3.3 | Spark | Procesamiento distribuido |
| 3.1 | Orquestación con Airflow | Coordinación del pipeline |
| 3.2 | Orquestación con Airflow | Coordinación del pipeline |
| 4.3 | Observabilidad + ML/IA | Monitoreo + consumidor ML |
| 4.2 | Despliegue en GCP y AWS | Puesta en producción |
| [pendiente] | [pendiente] | [pendiente] |
| [pendiente] | [pendiente] | [pendiente] |

> ⚠️ **Nota:** Los números de sesión en el diagrama no siguen un orden estrictamente lineal (aparecen 1.2, 1.3, 4.1, luego 2.1, 2.2…). Esto sugiere que el curso agrupa por **fases del pipeline** más que por secuencia numérica. Conviene aclararlo con el profesor.

---

## 13. RELACIÓN CON LOS CURSOS ANTERIORES

| Curso Previo | Qué Aporta a Este Curso |
|--------------|-------------------------|
| **Programación en Python** | Base de sintaxis, funciones, módulos |
| **Análisis de Datos en Python** | pandas, polars, manipulación de DataFrames |
| **Bases de Datos y SQL** | PostgreSQL, SQLite, consultas, modelado relacional, ACID |
| **Pipelines y ETL (este curso)** | Integra todo en un flujo automatizado de producción |

> 💡 **Clave:** Este curso es la **culminación** de la certificación: toma Python + análisis + SQL y los convierte en un pipeline real.

---

## 14. RESUMEN DE LA SESIÓN

### 📌 Lecciones Aprendidas

1. El curso se estructura como **un solo pipeline construido en 14 sesiones** (caso integrador: tienda en línea).
2. **¿Qué es un pipeline de datos?** Una secuencia automatizada de pasos que mueven el dato desde sus fuentes hasta sus consumidores finales, transformándolo en el camino, de forma repetible, observable y confiable.
3. **Ciclo de vida de la ingeniería de datos (Reis & Housley, 2022):** Generación → Ingesta → Transformación → Servicio → Consumidores (analítica, ML, ETL inverso). El **almacenamiento** atraviesa todas las etapas, y las **corrientes de fondo** (seguridad, gestión de datos, DataOps, arquitectura, orquestación e ingeniería de software) sostienen el ciclo completo.
4. La arquitectura sigue el patrón **Medallion (arquitectura de medallas)**: Bronze → Silver → Gold.
5. **Buenas prácticas de un pipeline de producción:**
   1. 🔁 **Idempotente** — correrlo N veces da el mismo resultado
   2. 🔄 **Reprocesable** — se puede volver a correr tras falla o backfill
   3. 🧱 **Atómico** — todo o nada, sin estados intermedios
   4. 👁️ **Observable** — métricas, logs y validaciones visibles
   5. 🧪 **Probado** — tests unitarios, integración y calidad de datos
   6. 🔒 **Seguro** — cifrado, control de acceso, PII protegida
6. Hay **cuatro fuentes heterogéneas**: PostgreSQL, API REST, CSV y eventos.
7. Los consumidores finales son un **tablero**, modelos de **ML/IA** y **ETL inverso**.
8. La capa transversal incluye **orquestación (Airflow)**, **observabilidad** y **despliegue en GCP/AWS**.
9. **Idempotencia en una imagen:** `INSERT` ciego duplica; `DELETE + INSERT` dentro de `BEGIN ... COMMIT` reemplaza la partición de forma idempotente y atómica.
10. **Escalabilidad:** se logra con particionamiento, paralelización, procesamiento incremental y cómputo distribuido (Spark).
11. La **ficha de 6 puntos** se aplica también al concepto de pipeline, no solo a motores de BD.

### 🗂️ Estructura Conceptual del Curso

```
📁 Caso Integrador: Analítica de una Tienda en Línea
├── 📥 Ingesta (PostgreSQL, API REST, CSV, Eventos)
├── 🥉 Bronze (datos crudos)
├── 🥈 Silver (limpios y validados)  ← Calidad del dato
├── 🥇 Gold (listos para consumir)
├── 📊 Consumidores: Tablero + ML/IA + ETL inverso
└── ⚙️ Transversal: Airflow · Observabilidad · GCP/AWS

Buenas prácticas transversales:
🔁 Idempotente · 🔄 Reprocesable · 🧱 Atómico · 👁️ Observable · 🧪 Probado · 🔒 Seguro
```

### 🎯 Preparado para la Próxima Sesión

- ✅ Caso integrador entendido
- ✅ Marco de referencia (ciclo de vida) internalizado
- ✅ Arquitectura Medallion identificada
- ✅ Buenas prácticas de producción documentadas
- ✅ Fuentes y consumidores mapeados
- ✅ Ficha de 6 puntos del pipeline completada
- ⏳ Pendiente: numeración exacta de las 14 sesiones y criterios de evaluación

---

**Nota final:** *"Este curso no enseña herramientas sueltas: enseña a construir un pipeline completo y de producción. Cada sesión es una pieza, y el caso integrador (la tienda en línea) es el hilo conductor que da sentido a todo."*

---