# Entorno de Desarrollo para Ingeniería de Datos

Este repositorio contiene una estructura de Data lab para proyectos de ingenieria de datos

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera para seguir las mejores prácticas de la industria:

```
.
├── data/               # Contiene todos los datasets del proyecto
│   ├── raw/            # Datos originales, sin procesar.
│   ├── processed/      # Datos intermedios, limpios y transformados.
│   └── curated/        # Datos finales, listos para análisis o consumo.
│
├── notebooks/          # Jupyter Notebooks para exploración y prototipado.
│   ├── exploration/    # Análisis exploratorio de datos (EDA).
│   └── prototypes/     # Prototipos de código o modelos antes de pasarlos a scripts.
│
├── src/                # Código fuente principal de los pipelines y la lógica de negocio.
│   ├── pipelines/      # Scripts que definen los pipelines de ETL.
│   └── utils/          # Funciones de utilidad reutilizables (ej. calidad de datos, conexión).
│
├── tests/              # Pruebas unitarias y de integración para asegurar la calidad del código.
│
├── homeworks/          # Tareas y ejercicios del curso. Cada tarea en su propia carpeta.
│
├── clases/             # Material y notebooks directamente relacionados con las clases.
│
├── projects/           # Proyectos de análisis end-to-end independientes.
│   └── nyc-accidents/  # Análisis de accidentes de tráfico en NYC.
│       ├── data/       # Datos específicos del proyecto (raw, processed, curated).
│       ├── notebooks/  # Notebooks de exploración y prototipos del proyecto.
│       ├── src/        # Pipelines y utilidades propias del proyecto.
│       └── tests/      # Pruebas del proyecto.
│
├── docker-compose.yml  # Orquestación de contenedores (ej. servicios de base de datos, etc.).
├── Dockerfile          # Definición del entorno de ejecución en un contenedor.
├── requirements.txt    # Dependencias de Python del proyecto.
└── README.md           # Este archivo.
```

## Cómo Empezar

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd data-engineering-certification
    ```

2.  **Crear un entorno virtual e instalar dependencias:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Ejecutar un pipeline (Ejemplo):**
    ```bash
    python src/main.py --pipeline=nombre_del_pipeline
    ```

## Inicio Rápido con Docker y Jupyter

El proyecto incluye un `Dockerfile` propio con Python 3.11, PySpark y JupyterLab, y un `docker-compose.yml` que orquesta además PostgreSQL, MongoDB y Redis.

### Primera vez (build obligatorio)

1.  **Construir la imagen personalizada:**
    ```bash
    docker compose build
    ```
    > Esto descarga la imagen base, instala dependencias del sistema, Java 17, y todos los paquetes de `requirements.txt`. Solo es necesario la primera vez o cuando cambies el `Dockerfile` o `requirements.txt`.

2.  **Levantar todos los servicios:**
    ```bash
    docker compose up -d
    ```

### Usos posteriores (sin rebuild)

1.  **Levantar servicios:**
    ```bash
    docker compose up -d
    ```

2.  **Abrir JupyterLab en el navegador:**

    [http://localhost:8888/lab](http://localhost:8888/lab)

3.  **Abrir el notebook de la Tarea 1:**

    [notebooks/exploration/Tarea1_Exploracion.ipynb](notebooks/exploration/Tarea1_Exploracion.ipynb)

> Importante: crea y guarda notebooks dentro de [notebooks](notebooks) o [homeworks](homeworks). Si guardas archivos fuera de `/workspace` dentro del contenedor, no quedan en tu proyecto local.

4.  **Usar datasets desde la carpeta raw:**

    [data/raw](data/raw)

5.  **Guardar entregables en:**

    [homeworks/output/tarea_1](homeworks/output/tarea_1)

### ¿Programo en VS Code o en el navegador?

- Para exploración y análisis inicial: JupyterLab en navegador.
- Para dejar código reutilizable y limpio: VS Code en scripts dentro de [src/pipelines](src/pipelines).
- Puedes mezclar ambos: el volumen Docker monta el proyecto completo y los cambios se reflejan en ambos lados.

## Servicios Disponibles con Docker

Cuando levantas el entorno con `docker compose up -d`, los siguientes servicios están disponibles:

| Servicio | URL / Puerto | Credenciales (por defecto) |
|:---------|:-------------|:---------------------------|
| **JupyterLab** | [http://localhost:8888](http://localhost:8888) | Sin contraseña |
| **PostgreSQL** | `localhost:5432` | Usuario: `datacourse` / Contraseña: `datacourse123` / Base de datos: `dataengineering` |
| **MongoDB** | `localhost:27017` | Usuario: `datacourse` / Contraseña: `datacourse123` |
| **Redis** | `localhost:6379` | Sin autenticación |

## Comandos Útiles de Docker

| Acción | Comando |
|:-------|:--------|
| Construir la imagen | `docker compose build` |
| Levantar todos los servicios | `docker compose up -d` |
| Ver logs en tiempo real | `docker compose logs -f` |
| Detener todos los servicios | `docker compose down` |
| Detener y eliminar volúmenes (borra datos) | `docker compose down -v` |
| Entrar al contenedor de Jupyter | `docker exec -it data_engineer_course bash` |
| Ver los contenedores en ejecución | `docker ps` |

### Proyecto: Análisis de Accidentes de Tráfico en NYC

1.  **Accede al notebook de exploración:**
    [projects/nyc-accidents/notebooks/exploration/01_EDA_Accidentes_NYC.ipynb](projects/nyc-accidents/notebooks/exploration/01_EDA_Accidentes_NYC.ipynb)

2.  **Coloca el dataset en:** `projects/nyc-accidents/data/raw/`