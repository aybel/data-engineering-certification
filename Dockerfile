FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Actualizar e instalar dependencias del sistema (VERSIÓN CORREGIDA)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    vim \
    git \
    tree \
    postgresql-client \
    redis-tools \
    gcc \
    g++ \
    make \
    libpq-dev \
    # Reemplazar mongodb-clients (ya no existe en repositorios nuevos)
    && apt-get install -y --no-install-recommends mongodb-mongosh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Java para Spark
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jdk-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

WORKDIR /workspace

# Crear usuario no root
RUN useradd -m -u 1000 -s /bin/bash datacourse && \
    chown -R datacourse:datacourse /workspace

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Instalar paquetes adicionales
RUN pip install --no-cache-dir pyspark==3.4.1 jupyterlab

# Cambiar al usuario no root
USER datacourse

# Exponer puertos
EXPOSE 8888 4040

# Comando por defecto
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]