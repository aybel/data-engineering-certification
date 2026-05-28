# Curso de Ingeniería de Datos - Tareas


# Tarea 1: Análisis de Calidad de Datos
**Objetivo:** Identificar y cuantificar todos los problemas en los datos

**Contexto:** Antes de construir un pipeline, necesitas entender la magnitud
de los problemas de calidad de datos.

### Tareas a realizar:
1. Lee el archivo '.csv' generado
2. Calcula y muestra:
   - Total de registros
   - Total de registros únicos (sin duplicados)
   - Cantidad y porcentaje de nulos por columna
   - Tipos de datos actuales vs esperados
3. Identifica transacciones con problemas específicos:
   - Montos negativos
   - Montos como string (con $)
   - Fechas en formato incorrecto
4. Genera un resumen en formato tabla

Pista: Usa pandas o Python puro según prefieras


## Tarea 2: Limpieza y Estandarización de Datos
**Objetivo:** Corregir todos los problemas de calidad identificados en la Tarea 1.

### Ejercicios:
- Implementar función `limpiar_montos()` que convierta a float, elimine $, corrija negativos y maneje nulos.
- Implementar función `estandarizar_fechas()` que unifique formato a YYYY-MM-DD.
- Implementar función `corregir_estados()` que asigne 'DESCONOCIDO' a valores vacíos.
- Implementar función `corregir_tiendas()` que asigne 'TIENDA_SIN_ESPECIFICAR' a nulos.
- Implementar función `corregir_clientes()` que asigne 'DESCONOCIDO' a nulos.
- Aplicar todas las funciones al dataset.
- Guardar resultado como `transacciones_clean.csv`.
- Generar reporte comparativo antes/después de la limpieza.

### Entregables:
- `src/pipelines/limpieza_datos.py` o notebook en `notebooks/prototypes`
- `homeworks/output/tarea_2/transacciones_clean.csv`
- `homeworks/output/tarea_2/reporte_limpieza.json`

## Tarea 3: Manejo de Valores Nulos y Duplicados
**Objetivo:** Implementar estrategias avanzadas para datos faltantes y eliminar duplicados.

### Ejercicios:
- Analizar patrones de nulos (¿hay correlación entre columnas?).
- Para `customer_id` nulos, intentar inferir por transacciones de la misma tienda/fecha.
- Para `amount` nulos, probar diferentes estrategias: media, mediana, valor anterior.
- Decidir cuál estrategia es mejor y justificar por qué.
- Eliminar duplicados exactos y por `transaction_id`.
- Enriquecer datos agregando columnas:
    - `mes` (extraído de fecha)
    - `trimestre`
    - `dia_semana`
    - `rango_monto` (bajo, medio, alto)
- Guardar resultado como `transacciones_enriched.csv`.

### Entregables:
- `src/pipelines/manejo_nulos_duplicados.py`
- `data/processed/transacciones_enriched.csv`
- `homeworks/output/tarea_3/analisis_nulos.txt` (con justificación de estrategias)

## Tarea 4: Validación y Control de Calidad
**Objetivo:** Implementar sistema de reglas de validación robusto.

### Reglas de negocio a implementar:
- `transaction_id` debe tener formato TXN-XXXXX (5 dígitos).
- `date` debe ser año 2023 en formato YYYY-MM-DD.
- `customer_id` no puede ser nulo (rechazar si lo es).
- `amount` debe estar entre 10 y 500.
- `status` solo: COMPLETADA, PENDIENTE, FALLIDA, CANCELADA.
- `store` no puede ser nulo.

### Ejercicios:
- Crear función `validar_registro(registro)` que retorne `(is_valid, lista_errores)`.
- Clasificar errores en CRÍTICOS (rechazar) vs ADVERTENCIAS (permitir).
- Separar dataset en:
    - `transacciones_validas.csv`
    - `transacciones_rechazadas.csv`
- Generar reporte de calidad con:
    - Porcentaje de registros válidos.
    - Top errores más frecuentes.
    - Estadísticas por tipo de error.

### Entregables:
- `src/pipelines/sistema_validacion.py`
- `data/curated/transacciones_validas.csv`
- `data/curated/transacciones_rechazadas.csv`
- `homeworks/output/tarea_4/reporte_validacion.json`

## Tarea 5: KPIs y Métricas de Negocio
**Objetivo:** Calcular indicadores clave a partir de los datos limpios.

### Ejercicios:
- **Métricas generales:**
    - Total ventas
    - Ticket promedio
    - Monto total por mes
- **Análisis por tienda:**
    - Top tienda por ventas
    - Tienda con mayor ticket promedio
    - Distribución por estado por tienda
- **Análisis de clientes:**
    - Top 5 clientes por gasto total
    - Clientes recurrentes (más de 1 compra)
    - Tasa de retención (aproximada)
- **Análisis temporal:**
    - Mes con mayores ventas
    - Día con más transacciones
    - ¿Hay tendencia de crecimiento?
- **Crear visualizaciones:**
    - Gráfico de barras (ventas por tienda)
    - Línea de tiempo (ventas por mes)
    - Pie chart (distribución por estado)
    - Histograma (distribución de montos)

### Entregables:
- `src/pipelines/calculadora_kpis.py`
- `homeworks/output/tarea_5/kpi_report.json`
- `homeworks/output/tarea_5/visualizaciones/` (carpeta con gráficos)

## Tarea 6: Pipeline Automatizado
**Objetivo:** Integrar todas las funciones anteriores en una clase `Pipeline` reutilizable.

### Ejercicios:
- Crear clase `DataPipeline` con métodos:
    - `extract()` - leer CSV
    - `transform()` - limpiar y estandarizar
    - `validate()` - aplicar reglas de negocio
    - `enrich()` - agregar columnas calculadas
    - `load()` - guardar en múltiples formatos
    - `run()` - ejecutar todo el flujo
- Agregar logging (info, warning, error).
- Hacer configurable vía archivo `config.yaml`:
    - Rutas de input/output
    - Umbrales de validación
    - Estrategias de limpieza
- Generar reporte HTML con resumen del pipeline.
- Manejar errores gracefully (no detener el pipeline por un registro malo).

### Entregables:
- `src/pipelines/data_pipeline.py`
- `homeworks/tarea_6/config.yaml`
- `logs/pipeline.log`
- `homeworks/output/tarea_6/reporte_pipeline.html`

## Tarea 7: Tests Unitarios
**Objetivo:** Asegurar que cada componente del pipeline funciona correctamente.

### Ejercicios:
- **Tests para funciones de limpieza:**
    - `test_corregir_monto()`
    - `test_estandarizar_fecha()`
    - `test_corregir_estado()`
- **Tests para validación:**
    - `test_validar_id_correcto()`
    - `test_validar_id_incorrecto()`
    - `test_validar_monto_fuera_rango()`
- **Tests para el pipeline:**
    - `test_pipeline_flujo_completo()`
    - `test_manejo_dataset_vacio()`
    - `test_manejo_datos_corruptos()`
- Lograr al menos 80% de cobertura de código.

### Entregables:
- `tests/test_pipeline.py`
- `homeworks/output/tarea_7/coverage_report.html`
- `homeworks/output/tarea_7/test_results.xml`

## Tarea 8: Proyecto Integrador Final
**Objetivo:** Construir un pipeline completo y desplegable.

### Ejercicios:
- Generar dataset más grande (1000+ registros).
- Implementar pipeline completo con todas las etapas.
- Agregar nuevas funcionalidades:
    - Detección de outliers (IQR o Z-score)
    - Corrección automática vs manual
    - Dashboard interactivo básico (con streamlit o similar)
- Exportar a múltiples formatos:
    - CSV (datos procesados)
    - Parquet (optimizado para consultas)
    - JSON (métricas para API)
- Crear documentación del pipeline (README técnico).
- (Opcional) Automatizar ejecución diaria con `schedule` o `cron`.

### Entregables:
- `src/main.py` (integrando el pipeline final)
- `src/dashboard.py` (opcional)
- `data/curated/final/` (todos los datasets procesados)
- `README.md` (actualizado con la documentación del pipeline)

## Estructura de carpetas (Referencia anterior)
```text
homeworks/
├── data/
│   └── transacciones_raw.csv
...
```

> **Nota:** La estructura de carpetas anterior ha sido actualizada a una versión más profesional. Consulta el `README.md` principal para ver la nueva organización.

## Checklist de progreso
| Tarea | Descripción | Estado | Puntos | Fecha |
|-------|-------------|--------|--------|-------|
| 1 | Exploración y Calidad | ✅ | 10 | 2026-05-05 |
| 2 | Limpieza de Datos | ⬜ | 15 | — |
| 3 | Manejo de Nulos/Duplicados | ⬜ | 15 | — |
| 4 | Validación y Calidad | ⬜ | 20 | — |
| 5 | KPIs y Métricas | ⬜ | 20 | — |
| 6 | Pipeline Automatizado | ⬜ | 25 | — |
| 7 | Tests Unitarios | ⬜ | 15 | — |
| 8 | Proyecto Integrador | ⬜ | 30 | — |

**Total:** 0/150 puntos
