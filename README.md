# Data Engineering Certification: entorno de práctica

Repositorio de trabajo para el curso de Ingeniería de Datos: material de clases, tareas, notas de los cursos y proyectos prácticos. Incluye un entorno reproducible con Docker (JupyterLab, PostgreSQL, MongoDB y Redis).

## Estructura del proyecto

```
.
├── clases/             # Notebooks de clase (Clase1.2.1, Clase122, ...) y sus datos.
│   └── data/
│
├── courses/            # Material de cada curso (apuntes, workbooks, código de ejemplo).
│   ├── 04_sql_python/      # Bases de datos y SQL con Python (SQLite, PostgreSQL, MongoDB, Redis, BigQuery).
│   │   ├── workbooks/      # Una guía .md por sesión.
│   │   ├── src/            # Código de apoyo (database, queries, utils).
│   │   └── tests/
│   └── pipelines_python/   # Pipelines con Python (sesion_01.md a sesion_04.md).
│
├── homeworks/          # Tareas del curso.
│   ├── database/           # Ejercicios de SQL/SQLite (exercise_01 ... 06) y su README con el enunciado.
│   ├── programming/        # Tareas de pipelines (tarea_1 ... tarea_3) y su README con el enunciado.
│   └── output/             # Resultados y reportes generados por las tareas.
│
├── projects/           # Proyectos independientes de punta a punta.
│   ├── nyc-accidents/      # Análisis de accidentes de tráfico en NYC (ver su README).
│   │   ├── data/           # raw, bronze, silver, quarantine, processed, curated.
│   │   ├── notebooks/      # exploration/ y prototypes/.
│   │   ├── src/            # pipelines/ (raw_a_bronze, bronze_a_silver) y utils/.
│   │   └── tests/
│   └── bd_etl_project/     # Esqueleto de un proyecto ETL (aún sin contenido).
│
├── data/               # Datasets compartidos por las tareas y notebooks de la raíz.
│   ├── raw/                # Datos originales (no se modifican).
│   ├── processed/          # Datos limpios o transformados.
│   └── generar_dataset.py  # Genera el dataset de transacciones usado en las tareas.
│
├── notebooks/          # Notebooks de exploración de la raíz.
│   └── exploration/        # Ej.: Tarea1_Exploracion.ipynb.
│
├── src/                # Librería compartida entre cursos, tareas y proyectos (ver "Dónde va el código").
│   ├── pipelines/          # Pipelines de ETL (por ahora vacío).
│   └── utils/              # data_loader.py (rutas de datos) y db_connections.py (conexiones a BD).
│
├── tests/              # Pruebas del código de src/.
├── scripts/            # Scripts auxiliares (entrypoint.sh).
│
├── .devcontainer/            # Configuración de Dev Container para VS Code.
├── .env.example              # Plantilla de variables de entorno.
├── docker-compose.yml        # Servicios: JupyterLab, PostgreSQL, MongoDB, Redis.
├── Dockerfile                # Imagen de Python 3.11 con requirements-dev.txt.
├── requirements.txt          # Dependencias base (las que instala la imagen).
├── requirements-dev.txt      # Base + pytest, black, flake8, mypy, pre-commit.
├── requirements-optional.txt # Paquetes pesados o aún sin uso (dbt, Prefect, Snowflake, ...).
└── README.md                 # Este archivo.
```

Cada carpeta principal con un README propio (`data/`, `notebooks/`, `projects/`, `scripts/`, `courses/*`, `homeworks/*`, `projects/nyc-accidents/`) amplía su contenido.

## Cómo empezar

### Opción A: Docker (recomendada)

Requiere Docker con el plugin `docker compose`.

1.  **Crear el archivo de variables de entorno (opcional):**
    ```bash
    cp .env.example .env
    ```
    `.env` está en `.gitignore`. Los valores por defecto del código coinciden con los de `docker-compose.yml`, así que solo necesitas editarlo si cambias credenciales o usas servicios en la nube.

2.  **Construir la imagen (primera vez, o al cambiar `Dockerfile` o los `requirements*.txt`):**
    ```bash
    docker compose build
    ```

3.  **Levantar los servicios:**
    ```bash
    docker compose up -d
    ```

4.  **Abrir JupyterLab:** [http://localhost:8888/lab](http://localhost:8888/lab) (sin contraseña ni token).

El proyecto completo se monta en `/workspace` dentro del contenedor. Guarda tus notebooks y archivos dentro de esa ruta, porque lo que se guarde fuera no aparece en tu carpeta local.

### Opción B: entorno virtual local

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt  # base + herramientas de desarrollo
```

Con esta opción los servicios de bases de datos no se levantan solos. Puedes iniciar solo los que necesites con `docker compose up -d postgres mongodb redis`.

> **Nombres de host:** dentro del contenedor de Jupyter los servicios se llaman `postgres`, `mongodb` y `redis` (los valores por defecto de `src/utils/db_connections.py`). Desde tu máquina usa `localhost`, por ejemplo `POSTGRES_HOST=localhost` en `.env`.

## Servicios disponibles con Docker

| Servicio | URL / Puerto | Credenciales (solo desarrollo local) |
|:---------|:-------------|:-------------------------------------|
| **JupyterLab** | [http://localhost:8888](http://localhost:8888) | Sin contraseña |
| **PostgreSQL 16** | `localhost:5432` | Usuario `datacourse` / Contraseña `datacourse123` / BD `dataengineering` |
| **MongoDB 6** | `localhost:27017` | Usuario `datacourse` / Contraseña `datacourse123` |
| **Redis 7** | `localhost:6379` | Sin autenticación |

Estas credenciales son únicamente para el entorno local del curso. No las reutilices en otros entornos.

## Comandos útiles de Docker

| Acción | Comando |
|:-------|:--------|
| Construir la imagen | `docker compose build` |
| Levantar todos los servicios | `docker compose up -d` |
| Ver logs en tiempo real | `docker compose logs -f` |
| Detener todos los servicios | `docker compose down` |
| Detener y eliminar volúmenes (borra los datos de PostgreSQL) | `docker compose down -v` |
| Entrar al contenedor de Jupyter | `docker exec -it data_engineer_course bash` |
| Ver los contenedores en ejecución | `docker ps` |

## Datos

- Los datasets de `data/raw/` y `projects/nyc-accidents/data/raw/*.csv|xlsx` están en `.gitignore` porque algunos pesan cientos de MB (por ejemplo `Motor_Vehicle_Collisions.csv`, unos 400 MB). Descárgalos por separado y colócalos en esas rutas.
- `data/generar_dataset.py` genera el dataset de transacciones de las tareas. El script escribe en `homeworks/data/transacciones_raw.csv` (carpeta que ya no existe), así que créala antes de ejecutarlo o cambia la ruta de salida a `data/raw/transacciones_raw.csv`.

## Trabajo en cada parte del repositorio

### Tareas

-   Enunciados: [homeworks/database/README.md](homeworks/database/README.md) y [homeworks/programming/README.md](homeworks/programming/README.md).
-   Primer notebook de exploración: [notebooks/exploration/Tarea1_Exploracion.ipynb](notebooks/exploration/Tarea1_Exploracion.ipynb).
-   Entregables y reportes en [homeworks/output](homeworks/output).

### Proyecto: análisis de accidentes de tráfico en NYC

-   Descripción y plan por fases: [projects/nyc-accidents/README.md](projects/nyc-accidents/README.md).
-   Notebooks: [projects/nyc-accidents/notebooks/exploration](projects/nyc-accidents/notebooks/exploration).
-   Dataset en `projects/nyc-accidents/data/raw/`.
-   Los pipelines `raw_a_bronze.py` y `bronze_a_silver.py` están en desarrollo (el primero es un borrador y el segundo está vacío). Usan rutas relativas a la raíz del repositorio, así que ejecútalos desde ahí.

### ¿JupyterLab o VS Code?

-   Exploración y análisis inicial: notebooks en JupyterLab.
-   Código reutilizable: scripts en VS Code dentro de `src/` (o en el `src/` del proyecto correspondiente).
-   Se pueden combinar, porque el volumen de Docker refleja los cambios en ambos lados.

## Dependencias

| Archivo | Contenido | Se instala en la imagen |
|:--------|:----------|:------------------------|
| `requirements.txt` | Librerías de datos, visualización, bases de datos y Jupyter | Sí |
| `requirements-dev.txt` | Lo anterior más pytest, black, flake8, mypy y pre-commit | Sí |
| `requirements-optional.txt` | dbt, Great Expectations, Dask, Prefect, Snowflake, boto3, FastAPI, etc. | No |
| `courses/<curso>/requirements.txt` | Lo específico de un curso (por ejemplo Airflow y PySpark en `pipelines_python`) | No |

Los paquetes pesados no están en la imagen porque no se usan todavía y es probable que choquen con las versiones fijadas del resto. Instala los de un curso cuando llegues a esa sesión:

```bash
docker exec -it data_engineer_course pip install -r courses/pipelines_python/requirements.txt
```

Airflow tiene instrucciones propias de instalación dentro de ese archivo. PySpark necesita Java, que la imagen no incluye.

Dos versiones están acotadas a propósito: `pyarrow<15` (las versiones nuevas exigen NumPy 2 y el proyecto usa NumPy 1.24.3) y `pandera<0.24` (los apuntes usan `from pandera import DataFrameSchema`, que las versiones nuevas ya no permiten).

## Dónde va el código

| Ubicación | Qué va ahí |
|:----------|:-----------|
| `src/utils/`, `src/pipelines/` (raíz) | Código reutilizable por más de un curso, tarea o proyecto, y los pipelines que piden los enunciados de `homeworks/programming`. Ej.: `data_loader.py`, `db_connections.py`. |
| `projects/<proyecto>/src/` | Código que solo sirve a ese proyecto. |
| `courses/<curso>/src/` | Ejemplos de apoyo de ese curso. No lo importes desde fuera del curso. |

Si algo de un proyecto o curso termina usándose en otro, muévelo a `src/` de la raíz. Los notebooks encuentran la librería compartida buscando hacia arriba la carpeta que contiene `src/utils/data_loader.py`. Evita dar a los módulos de un proyecto el mismo nombre de paquete que los de la raíz (por ejemplo, otro paquete `utils`), porque Python solo importaría uno de los dos.

## Calidad de código

Las dependencias incluyen `pytest`, `black`, `flake8` y `mypy`:

```bash
pytest                 # pruebas
black .                # formato
flake8 src             # estilo
```
