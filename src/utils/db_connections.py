"""
src/utils/db_connections.py
Utilidades de conexión a bases de datos para el curso de BD con Python
"""

import os
import sqlite3
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
from pymongo import MongoClient
import redis
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ============================================
# CONFIGURACIÓN DE SERVICIOS (desde .env)
# ============================================

POSTGRES_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'dataengineering'),
    'user': os.getenv('POSTGRES_USER', 'datacourse'),
    'password': os.getenv('POSTGRES_PASSWORD', 'datacourse123')
}

MONGODB_CONFIG = {
    'host': os.getenv('MONGODB_HOST', 'mongodb'),
    'port': int(os.getenv('MONGODB_PORT', '27017')),
    'user': os.getenv('MONGODB_USER', 'datacourse'),
    'password': os.getenv('MONGODB_PASSWORD', 'datacourse123')
}

REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'redis'),
    'port': int(os.getenv('REDIS_PORT', '6379')),
    'decode_responses': True
}

# ============================================
# POSTGRESQL
# ============================================

def get_postgres_url():
    """Retorna URL de conexión para SQLAlchemy"""
    return f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}"

def get_postgres_engine():
    """Retorna engine SQLAlchemy para PostgreSQL"""
    return create_engine(get_postgres_url())

def get_postgres_connection():
    """Retorna conexión directa psycopg2 para PostgreSQL"""
    return psycopg2.connect(**POSTGRES_CONFIG)

def read_sql_to_df(query, params=None):
    """
    Ejecuta query SQL y retorna DataFrame de Pandas
    
    Args:
        query (str): Consulta SQL
        params (tuple, optional): Parámetros para query parametrizada
    
    Returns:
        pd.DataFrame: Resultado de la consulta
    """
    engine = get_postgres_engine()
    return pd.read_sql_query(query, engine, params=params)

def write_df_to_table(df, table_name, if_exists='replace', index=False):
    """
    Escribe un DataFrame a una tabla en PostgreSQL
    
    Args:
        df (pd.DataFrame): DataFrame a escribir
        table_name (str): Nombre de la tabla
        if_exists (str): 'fail', 'replace', 'append'
        index (bool): Incluir índice como columna
    """
    engine = get_postgres_engine()
    df.to_sql(table_name, engine, if_exists=if_exists, index=index)

# ============================================
# SQLITE (para desarrollo local)
# ============================================

def get_sqlite_connection(db_path='data/processed/local.db'):
    """Retorna conexión SQLite"""
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def read_sqlite_to_df(query, db_path='data/processed/local.db'):
    """Lee datos de SQLite a DataFrame"""
    with get_sqlite_connection(db_path) as conn:
        return pd.read_sql_query(query, conn)

# ============================================
# MONGODB
# ============================================

def get_mongo_client():
    """Retorna cliente de MongoDB"""
    return MongoClient(
        host=MONGODB_CONFIG['host'],
        port=MONGODB_CONFIG['port'],
        username=MONGODB_CONFIG['user'],
        password=MONGODB_CONFIG['password']
    )

def get_mongo_db(db_name='dataengineering'):
    """Retorna base de datos MongoDB"""
    client = get_mongo_client()
    return client[db_name]

def get_mongo_collection(collection_name, db_name='dataengineering'):
    """Retorna una colección de MongoDB"""
    db = get_mongo_db(db_name)
    return db[collection_name]

# ============================================
# REDIS
# ============================================

def get_redis_client():
    """Retorna cliente de Redis"""
    return redis.Redis(
        host=REDIS_CONFIG['host'],
        port=REDIS_CONFIG['port'],
        decode_responses=REDIS_CONFIG['decode_responses']
    )

def test_redis_connection():
    """Prueba conexión a Redis"""
    r = get_redis_client()
    r.set('test_connection', 'ok')
    result = r.get('test_connection')
    return result == 'ok'

# ============================================
# TEST DE CONEXIONES
# ============================================

def test_all_connections():
    """Prueba todas las conexiones"""
    results = {}
    
    # PostgreSQL
    try:
        engine = get_postgres_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        results['postgresql'] = '✅ OK'
    except Exception as e:
        results['postgresql'] = f'❌ Error: {e}'
    
    # SQLite
    try:
        with get_sqlite_connection(':memory:') as conn:
            conn.execute("SELECT 1")
        results['sqlite'] = '✅ OK'
    except Exception as e:
        results['sqlite'] = f'❌ Error: {e}'
    
    # MongoDB
    try:
        client = get_mongo_client()
        client.admin.command('ping')
        results['mongodb'] = '✅ OK'
    except Exception as e:
        results['mongodb'] = f'❌ Error: {e}'
    
    # Redis
    try:
        r = get_redis_client()
        r.ping()
        results['redis'] = '✅ OK'
    except Exception as e:
        results['redis'] = f'❌ Error: {e}'
    
    return results