# Proyecto de Ingeniería de Datos

Este repositorio contiene los materiales y ejercicios para un curso de ingeniería de datos.

## Descripción

El objetivo de este proyecto es proporcionar una base práctica en ingeniería de datos, cubriendo desde la limpieza y validación de datos hasta la creación de pipelines automatizados y el cálculo de KPIs.

## Estructura del Proyecto

-   `data/`: Contiene los datasets iniciales y procesados.
-   `docker-compose.yml`: Define los servicios, redes y volúmenes para el entorno de Docker.
-   `Dockerfile`: Contiene las instrucciones para construir la imagen de Docker para el entorno de desarrollo.
-   `generar_dataset.py`: Un script para generar datos de muestra para las tareas.
-   `homeworks/`: Contiene las tareas del curso. Cada tarea tiene su propia subcarpeta. El `README.md` dentro de esta carpeta tiene el detalle de cada tarea.
-   `notebooks/`: Jupyter notebooks para exploración de datos y análisis.
-   `projects/`: Proyectos integradores o finales.
-   `requirements.txt`: Lista de las dependencias de Python para el proyecto.
-   `scripts/`: Contiene scripts de utilidad, como el `entrypoint.sh` para el contenedor de Docker.

## Cómo Empezar

### Prerrequisitos

-   Docker
-   Python 3.8+

### Instalación y Ejecución

1.  **Construir y levantar el contenedor de Docker:**
    ```bash
    docker-compose up --build
    ```

2.  **Generar el dataset inicial:**
    Ejecuta el siguiente comando en tu terminal para generar el archivo `transacciones_raw.csv` en la carpeta `homeworks/data/`.
    ```bash
    python generar_dataset.py
    ```

3.  **Acceder al entorno:**
    Puedes acceder a los servicios definidos en `docker-compose.yml`, como un Jupyter Lab o un shell dentro del contenedor.
