# Análisis de Accidentes de Tráfico - NYC

## Objetivo del proyecto
Analizar los accidentes de tráfico en Nueva York para identificar patrones temporales, geográficos y factores de riesgo.

## Dataset
- Origen: NYC Open Data (Accidentes de tráfico)
- Tamaño: 475 MB
- Columnas principales: CRASH DATE, CRASH TIME, BOROUGH, LATITUDE, LONGITUDE, CONTRIBUTING FACTOR VEHICLE 1, NUMBER OF PERSONS INJURED, etc.

## Plan de acción

### Fase 1: Limpieza y exploración (Día 1)
- [ ] Cargar dataset con `pd.read_csv(low_memory=False)`
- [ ] Explorar estructura con `.info()`, `.describe()`, `.head()`
- [ ] Identificar columnas con nulos y decidir tratamiento
- [ ] Convertir fechas a datetime y extraer hora, día, mes
- [ ] Filtrar registros sin coordenadas
- [ ] Generar diccionario de los tipos de vehiculo

### Fase 2: Análisis exploratorio (Día 2)
- [ ] Crear mapa de calor de accidentes con `folium`
- [ ] Analizar distribución temporal (hora, día, mes)pe
- [ ] Identificar factores contribuyentes más comunes
- [ ] Explorar relación entre tipo de vehículo y severidad

### Fase 3: Feature Engineering y modelado (Día 3-4)
- [ ] Crear variable objetivo (severidad del accidente)
- [ ] Crear nuevas variables (hora, día, fin de semana, etc.)
- [ ] Entrenar modelo de clasificación (RandomForest o XGBoost)
- [ ] Evaluar modelo con validación cruzada

## Herramientas a utilizar
- Python (pandas, numpy, matplotlib, seaborn)
- `folium` o `plotly` para mapas interactivos
- `scikit-learn` para modelado