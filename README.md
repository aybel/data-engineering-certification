# Entorno de Desarrollo para Ingeniería de Datos

Este repositorio contiene una estructura de Data lab 

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

Si ya levantaste Docker sin errores, este es el flujo recomendado para empezar a trabajar:

1.  **Levantar servicios:**
    ```bash
    docker compose up -d
    ```

2.  **Abrir JupyterLab en el navegador:**

    [http://localhost:8888/lab](http://localhost:8888/lab)

3.  **Abrir el notebook de la Tarea 1:**

    [notebooks/exploration/Tarea1_Exploracion.ipynb](notebooks/exploration/Tarea1_Exploracion.ipynb)

> Importante: crea y guarda notebooks dentro de [notebooks](notebooks) o [homeworks](homeworks). Si guardas archivos fuera de `/home/jovyan/work` dentro del contenedor, no quedan en tu proyecto local.

4.  **Usar datasets desde la carpeta raw:**

    [data/raw](data/raw)

5.  **Guardar entregables en:**

    [homeworks/output/tarea_1](homeworks/output/tarea_1)

### ¿Programo en VS Code o en el navegador?

- Para exploración y análisis inicial: JupyterLab en navegador.
- Para dejar código reutilizable y limpio: VS Code en scripts dentro de [src/pipelines](src/pipelines).
- Puedes mezclar ambos: el volumen Docker monta el proyecto completo y los cambios se reflejan en ambos lados.
