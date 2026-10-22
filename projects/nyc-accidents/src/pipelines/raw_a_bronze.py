# projects/nyc-accidents/src/pipelines/raw_a_bronze.py

# Pipeline para mover datos de la capa raw a la capa bronze en el proyecto de accidentes de NYC


RAW    = Path("projects/nyc-accidents/data/raw/Motor_Vehicle_Collisions.csv")
BRONZE = Path("projects/nyc-accidents/data/bronze/Motor_Vehicle_Collisions.parquet")
BRONZE.parent.mkdir(parents=True, exist_ok=True)

# En este pipeline vamos a pasar de raw a bronze convirtiendo el csv a parquet para optimzar consultas