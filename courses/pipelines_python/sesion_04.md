# 📓 WORKBOOK - SESIÓN 1.3
## Capa Gold, Calidad de Datos y Contratos de Silver - Pipelines y ETL con Python

**Curso:** Pipelines y ETL con Python | BSG Institute
**Fecha:** 05/11/2026
**Duración:** [pendiente] (Sesión 3 de 14)

---

## 📌 ÍNDICE

1. [Panorama de la Sesión](#1-panorama-de-la-sesión)
2. [La Capa Gold y el Estándar DAMA](#2-la-capa-gold-y-el-estándar-dama)
3. [¿Quién Define los Contratos de Datos?](#3-quién-define-los-contratos-de-datos)
4. [El Contrato de Silver con Pandera](#4-el-contrato-de-silver-con-pandera)
5. [La Forma del Kit: Funciones Puras](#5-la-forma-del-kit-funciones-puras)
6. [Cuarentena de Datos: Apartar, No Tirar](#6-cuarentena-de-datos-apartar-no-tirar)
7. [Conexión con las Buenas Prácticas](#7-conexión-con-las-buenas-prácticas)
8. [Resumen de la Sesión](#8-resumen-de-la-sesión)

---

## 1. PANORAMA DE LA SESIÓN

### 🎯 Idea Central

> *"En Bronze la calidad es técnica; en Gold, la calidad es de negocio. DAMA nos da el vocabulario para medirla y Pandera nos da las herramientas para hacerla cumplir."*

Esta sesión profundiza en la **calidad de los datos** y en cómo se construye la capa **Gold**, aquella que alimenta los tableros y modelos de ML. También establece las bases de arquitectura de software para que el pipeline sea testeable y robusto.

### 📋 Los Temas de la Sesión

| # | Tema | Qué resuelve |
|---|------|--------------|
| 1 | **Capa Gold y DAMA** | Definir qué significa "calidad" para el negocio |
| 2 | **Roles de Gobernanza** | Saber quién define las reglas del juego |
| 3 | **Contratos con Pandera** | Implementar la validación técnica en Silver |
| 4 | **Funciones Puras** | Diseñar código testeable, determinista y sin efectos |
| 5 | **Cuarentena** | Manejar los errores sin detener el pipeline ni perder trazabilidad |

---

## 2. LA CAPA GOLD Y EL ESTÁNDAR DAMA

### 🥇 La Capa Gold en el Caso Integrador

La capa **Gold** contiene los datos **agregados, modelados y listos para consumir** por el negocio. Es la única capa que alimenta el **Tablero (2.2)** y los modelos de **ML/IA (4.3)**.

| Aspecto | Detalle |
|---------|---------|
| **Propósito** | Datos listos para análisis, reporting y ML |
| **Consumidores** | Analistas de negocio, tableros de BI, científicos de datos |
| **Riesgo principal** | Un defecto en Gold se convierte directamente en una **decisión de negocio equivocada** |

> 💡 **Clave:** Un pipeline puede correr "en verde" y aun así producir datos incorrectos en Gold. DAMA ayuda a definir **qué significa "correcto"**.

### 📖 ¿Qué es el Estándar DAMA?

**DAMA International** (Data Management Association) publica el **DAMA-DMBOK**, el marco de referencia más utilizado para la gestión de datos. Define la calidad como *"el grado en que las dimensiones de la calidad de los datos cumplen con los requisitos"*.

### 🧩 Las 6 Dimensiones Fundamentales de DAMA

En la práctica, estas son las dimensiones núcleo para medir la calidad:

| Dimensión | Pregunta que responde | Aplicación en la Capa Gold |
|-----------|----------------------|----------------------------|
| **1. Completitud** | ¿Están todos los datos necesarios? | ¿Todos los pedidos tienen `monto` y `cliente_id`? |
| **2. Unicidad** | ¿Hay duplicados? | ¿Un mismo `pedido_id` aparece más de una vez? |
| **3. Oportunidad** | ¿El dato está disponible cuando se necesita? | ¿El tablero está actualizado a las 8:00 AM? |
| **4. Validez** | ¿Cumple el formato, tipo y dominio definidos? | ¿El `estado` pertenece al dominio permitido? |
| **5. Precisión** | ¿Refleja la realidad del negocio? | ¿El `monto_total` coincide con la suma de las líneas? |
| **6. Consistencia** | ¿Concuerda entre tablas? | ¿El `pais` del cliente es igual al de envío? |

> 💡 **Clave:** DAMA no impone un número único de dimensiones. DAMA-DMBOK2 describe 15 en total, pero estas 6 fundamentales cubren el 90% de los casos prácticos.

---

## 3. ¿QUIÉN DEFINE LOS CONTRATOS DE DATOS?

> *"El contrato de datos no se programa: se negocia. El ingeniero es el notario que lo escribe en código, pero el negocio es el que dicta la ley."*

Un contrato de datos es un **acuerdo formal** entre quienes producen el dato, quienes lo gobiernan y quienes lo consumen.

### 👥 Los Roles Involucrados (Gobernanza DAMA)

| Rol | Quién es | Qué aporta al contrato |
|-----|----------|------------------------|
| **1. Data Owner** (Dueño) | Líder de negocio (ej. Dir. Ventas) | Aprueba el contrato y asume el riesgo. |
| **2. Data Steward** (Custodio) | Experto de negocio o analista senior | **Define las reglas**. Sabe qué es un dato válido. |
| **3. Data Engineer** (Ingeniero) | Tú, en este curso | **Traduce las reglas a código** (Pandera). |
| **4. Data Consumer** (Consumidor) | Científico de datos, equipo de BI | **Pide los requisitos** para que sus modelos funcionen. |

---

## 4. EL CONTRATO DE SILVER CON PANDERA

> *"Si Bronze preserva, Silver valida. Pandera es el guardián que no deja pasar basura a la capa Gold."*

**Pandera** es la librería que permite validar DataFrames de forma declarativa. La forma moderna de usarlo es mediante **clases** (`pa.DataFrameModel`), que se ven como código autodocumentado.

### 💻 El Ejemplo del Profesor (con Polars)

```python
import pandera as pa
import polars as pl

class PedidoSilver(pa.DataFrameModel):
    # 1. Validaciones a nivel de columna (Reglas simples)
    origen: str = pa.Field(isin=["web", "tienda"])
    pedido_id: int = pa.Field(gt=0)              # no nulo por omisión
    estado: str = pa.Field(isin=ESTADOS)
    total: float = pa.Field(gt=0, le=TOTAL_MAXIMO)
    moneda: str = pa.Field(isin=["MXN", "USD"])
    
    # 2. Tipos de datos estrictos
    creado_en: UTC
    actualizado_en: UTC

    # 3. Validación cruzada (Regla de negocio compuesta)
    @pa.dataframe_check(error="Llave (origen, pedido_id) duplicada")
    def llave_unica(cls, data):
        # Usa sintaxis de Polars para verificar duplicados en la llave compuesta
        return data.lazyframe.select(pl.struct("origen", "pedido_id")).is_duplicated().not_()

# Ejecución con lazy=True
PedidoSilver.validate(df, lazy=True)
```

### 🔍 Desglose del Ejemplo

| Elemento | Qué hace | Dimensión DAMA |
|----------|----------|----------------|
| `pa.Field(isin=[...])` | Define un dominio cerrado (ej. estados permitidos). | **Validez** |
| `pa.Field(gt=0)` | Valida que un número sea mayor a cero. | **Validez** |
| Nulos por omisión | Si no se pone `nullable=True`, Pandera rechaza los nulos. | **Completitud** |
| `@pa.dataframe_check` | Valida reglas entre múltiples columnas (ej. llave compuesta única). | **Unicidad** |
| `lazy=True` | Junta **todos** los errores antes de fallar. | **Observabilidad** |

> ⚠️ **Apunte clave:** El profesor usó `pl.struct` (Polars) dentro del check. Esto demuestra que el pipeline está optimizado para alto rendimiento, no solo para pandas. `lazy=True` es vital en producción para ver el panorama completo de errores de un solo golpe.

---

## 5. LA FORMA DEL KIT: FUNCIONES PURAS

> *"El secreto de un pipeline robusto está en separar la lógica de negocio (el 'qué') de la entrada/salida de datos (el 'dónde')."*

Para que el código sea testeable e idempotente, el pipeline se divide en tres zonas:

```
       ENTRADA (E/S)                   NÚCLEO (Lógica)                     SALIDA (E/S)
    ┌──────────────┐             ┌────────────────────────────┐        ┌──────────────┐
    │   leer.py    │             │     FUNCIONES PURAS        │        │ pipeline.py  │
    │              │  ────────>  │    DataFrame → DataFrame   │  ───>  │              │
    │ sabe dónde   │             │  ┌───────┐ ┌───────┐       │        │ orquesta y   │
    │ viven los    │             │  │limpieza│ │ dedup │ ...   │        │ publica      │
    │ archivos     │             │  └───────┘ └───────┘       │        │ todo o nada  │
    └──────────────┘             └────────────────────────────┘        └──────────────┘
```

### 🚫 Las Reglas de las Funciones Puras
Dentro del núcleo (`limpieza.py`, `dedup.py`, `calidad.py`, etc.):
*   **Sin archivos:** No leen ni escriben CSV/Parquet.
*   **Sin la hora del sistema:** No usan `datetime.now()` (rompe la idempotencia).
*   **Sin efectos secundarios:** No imprimen, no mandan correos, no tocan la base de datos.

> 💡 **Clave:** Al ser puras, son **deterministas**. Si les pasas el mismo DataFrame, devuelven exactamente el mismo DataFrame. Esto hace que las pruebas unitarias sean triviales (no necesitas mocks ni bases de datos, solo crear un DataFrame de prueba y validar la salida).

---

## 6. CUARENTENA DE DATOS: APARTAR, NO TIRAR

> *"Un dato que falla el contrato no es basura, es una señal de que algo pasó. Se aparta para investigar, no se borra."*

Cuando Pandera (con `lazy=True`) detecta filas que no cumplen el contrato, no se detiene todo el pipeline (Fail-fast), ni se descartan los datos. Se aplica la **Cuarentena**.

### 📋 Las Reglas de la Cuarentena

1.  **Guardar la fila completa:** Tal como venía, más dos columnas:
    *   `motivo`: El error exacto (ej. `estado: not_nullable`).
    *   `fecha_carga`: Cuándo falló.
2.  **Revisión con el Data Steward/Owner:** ¿Es un error de la fuente o la regla está mal escrita?
3.  **Resolución:**
    *   Si **falla la fuente:** Se corrige en origen. La próxima carga traerá el dato bueno y entrará solo (idempotencia).
    *   Si **falla la regla:** Se corrige el código de Pandera y se reprocesa desde Bronze.

### 📊 Ejemplo de Reporte de Cuarentena

El profesor mostró un reporte real del 22/09: *"tres problemas a la vez"*.

| motivo | filas | Dimensión DAMA |
|--------|-------|----------------|
| `total: less_than_or_equal_to(50000)` | 158 | **Validez** (Rango) |
| `estado: not_nullable` | 41 | **Completitud** |
| `moneda: not_nullable` | 27 | **Completitud** |
| `total: not_nullable` | 3 | **Completitud** |

> 💡 **Clave:** Gracias a `lazy=True`, el equipo vio los 3 problemas juntos en lugar de arreglarlos de uno en uno.

### 💻 Implementación de la Cuarentena

```python
def procesar_silver(df_bronze):
    try:
        # Intentamos validar todo de golpe
        df_silver = PedidoSilver.validate(df_bronze, lazy=True)
        return df_silver, None
        
    except pa.errors.SchemaErrors as err:
        # Pandera nos da un DataFrame con los errores
        df_errores = err.failure_cases
        indices_malos = df_errores["index"].unique()
        
        # Separamos: los buenos avanzan, los malos a cuarentena
        df_cuarentena = df_bronze.loc[indices_malos].copy()
        df_silver = df_bronze.drop(indices_malos)
        
        # Metadatos de cuarentena
        df_cuarentena["motivo"] = "Fallo de contrato"  # (Mapear de err.failure_cases)
        df_cuarentena["fecha_carga"] = pd.Timestamp.now()
        
        # Guardar
        df_cuarentena.to_parquet("silver/cuarentena/pedidos_20261001.parquet")
        
        return df_silver, df_cuarentena
```

---

## 7. CONEXIÓN CON LAS BUENAS PRÁCTICAS

Cómo se aplican las **seis buenas prácticas de la Sesión 1.1** en lo visto hoy:

| Práctica | Aplicación en Calidad y Silver |
|----------|--------------------------------|
| 🔁 **Idempotente** | Funciones puras (sin `datetime.now()`) garantizan mismo output. Reprocesar cuarentena no duplica. |
| 🔄 **Reprocesable** | Si la regla estaba mal, se corrige Pandera y se reprocesa desde Bronze. |
| 🧱 **Atómico** | `pipeline.py` publica todo o nada al final. |
| 👁️ **Observable** | `lazy=True` en Pandera da un reporte completo. El reporte de cuarentena muestra los motivos. |
| 🧪 **Probado** | Al tener funciones puras (`DataFrame -> DataFrame`), se testean en milisegundos. |
| 🔒 **Seguro** | Los contratos protegen la capa Gold de datos basura. |

---

## 8. RESUMEN DE LA SESIÓN

### 📌 Lecciones Aprendidas

1. **DAMA** es el estándar para medir calidad. Las 6 dimensiones clave son: Completitud, Unicidad, Oportunidad, Validez, Precisión y Consistencia.
2. **Gobernanza:** Los contratos no los inventa el ingeniero. Los define el negocio (Data Steward/Owner) y el ingeniero los codifica.
3. **Pandera** es la herramienta ideal para Silver. Usar `pa.DataFrameModel` es más limpio que diccionarios. `lazy=True` es obligatorio para ver todos los errores.
4. **Funciones Puras:** El código se divide en E/S (`leer.py`, `pipeline.py`) y Núcleo (`DataFrame -> DataFrame`). El núcleo no tiene archivos, ni hora, ni efectos.
5. **Cuarentena:** Las filas que fallan se apartan (con `motivo` y `fecha_carga`), no se borran. Permite corregir la fuente o la regla y reprocesar.

### 🗂️ Estructura Conceptual

```
🥇 CAPA GOLD (Consumo)
   ▲
   │ (Agregaciones)
🥈 CAPA SILVER (Limpieza y Calidad)
   │
   ├── 📜 Contratos Pandera (pa.DataFrameModel)
   │      └── @pa.dataframe_check + lazy=True
   │
   ├── 🧪 Funciones Puras (DataFrame → DataFrame)
   │      └── Sin archivos, sin reloj, sin efectos
   │
   └── 🚨 Cuarentena (Filas malas + motivo + fecha)
          └── Revisión con Data Steward
```

### 🎯 Preparado para la Próxima Sesión

- ✅ Estándar DAMA entendido
- ✅ Roles de gobernanza claros
- ✅ Contratos de Silver en Pandera implementados
- ✅ Arquitectura de Funciones Puras comprendida
- ✅ Estrategia de Cuarentena establecida
- ⏳ Pendiente: Implementación práctica del pipeline hacia Gold

---

**Nota final:** *"La calidad no es un accidente; es el resultado de diseñar contratos claros, funciones puras y un sistema que sepa apartar lo malo sin detener el flujo de lo bueno. En Gold, un dato malo cuesta dinero; en Silver, cuesta una alerta."*

---