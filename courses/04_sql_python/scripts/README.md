# Curso 04: Bases de Datos y SQL con Python

## 🎯 Objetivo del Curso
Este curso te proporcionará las habilidades para interactuar con bases de datos relacionales y NoSQL utilizando Python. Aprenderás a diseñar esquemas, escribir consultas SQL complejas y conectar tus aplicaciones de Python con sistemas de bases de datos.

## 📚 Temario

El curso está estructurado en 14 sesiones que cubren los fundamentos y técnicas avanzadas de SQL aplicadas en un contexto de ingeniería de datos.

| Sesión | Tema | Descripción |
|:-------|:-----|:------------|
| 1 | **Introducción a las Bases de Datos** | Conceptos fundamentales: sistemas de gestión de bases de datos (DBMS), bases de datos relacionales y NoSQL. |
| 2 | **Modelado de Datos y SQL Básico** | Diseño de esquemas, creación de tablas, y sentencias `SELECT`, `INSERT`, `UPDATE`, `DELETE`. |
| 3 | **Consultas con Filtros y Ordenamiento** | Uso de `WHERE`, `ORDER BY`, y operadores de comparación y lógicos. |
| 4 | **Funciones de Agregación y Agrupamiento** | Uso de `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` y la cláusula `GROUP BY`. |
| 5 | **Joins y Relaciones entre Tablas** | Combinación de datos de múltiples tablas usando `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN` y `FULL OUTER JOIN`. |
| 6 | **Subconsultas y Vistas** | Creación de consultas anidadas y uso de vistas para simplificar consultas complejas. |
| 7 | **Funciones de Ventana (Window Functions)** | Aplicación de funciones como `ROW_NUMBER`, `RANK`, `LAG`, y `LEAD` para análisis avanzado. |
| 8 | **Optimización de Consultas y Buenas Prácticas** | Uso de índices, análisis de planes de ejecución y técnicas para escribir consultas eficientes. |
| 9 | **Transacciones y Control de Concurrencia** | Gestión de transacciones usando `BEGIN`, `COMMIT`, `ROLLBACK` y conceptos de bloqueo. |
| 10 | **Introducción a SQLAlchemy** | Uso de SQLAlchemy como ORM y para crear conexiones a bases de datos desde Python. |
| 11 | **Bases de Datos NoSQL: MongoDB** | Inserción, consulta y agregación de datos en MongoDB desde Python con `pymongo`. |
| 12 | **Integración de Datos con Python** | Uso de `pandas` para leer/escribir datos en bases de datos y realizar transformaciones. |
| 13 | **Proyecto Guiado** | Aplicación de todos los conceptos en un caso práctico de ETL (Extracción, Transformación y Carga). |
| 14 | **Cierre y Proyecto Final** | Revisión de conceptos y espacio para completar el proyecto final del curso. |

## 🛠️ Entorno de Trabajo

Este curso está diseñado para ejecutarse en el entorno de desarrollo de este repositorio.

### Servicios disponibles (Docker)
- **PostgreSQL**: Base de datos relacional. `localhost:5432`
- **MongoDB**: Base de datos NoSQL. `localhost:27017`
- **Redis**: Sistema de caché y colas. `localhost:6379`
- **JupyterLab**: Entorno de desarrollo. `http://localhost:8888`

### Conexión desde Python
```python
# PostgreSQL con psycopg2
import psycopg2
conn = psycopg2.connect(
    host="postgres",
    database="dataengineering",
    user="datacourse",
    password="datacourse123"
)

# MongoDB con pymongo
import pymongo
client = pymongo.MongoClient("mongodb://datacourse:datacourse123@mongodb:27017")

courses/04_sql_python/
├── notebooks/       # Notebooks de las 14 sesiones
├── scripts/         # Scripts Python reutilizables (conexiones, funciones)
├── sql_scripts/     # Archivos .sql con consultas y esquemas
├── data/            # Datasets pequeños para los ejercicios
└── README.md        # Este archivo

📝 Instrucciones de Uso
Levanta el entorno: Desde la raíz del repositorio, ejecuta docker compose up -d.

Accede a JupyterLab: Abre http://localhost:8888 en tu navegador.

Crea tu notebook: Dentro de courses/04_sql_python/notebooks/, crea un notebook para la sesión que estés cursando (ej. sesion_01_introduccion.ipynb).

Practica: Sigue los ejercicios del curso y experimenta con las conexiones a las bases de datos.

🎓 Recursos Adicionales
Documentación de PostgreSQL

Documentación de MongoDB

SQLAlchemy Documentation

Documentación de pandas para bases de datos

