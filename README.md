# Proyecto del Curso de Ingeniería de Datos

Este repositorio contiene las tareas, proyectos y material de estudio para el curso de Ingeniería de Datos.

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
    cd data-engineer-course
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
