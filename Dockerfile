FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Actualizar e instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    vim \
    git \
    tree \
    gnupg \
    postgresql-client \
    redis-tools \
    gcc \
    g++ \
    make \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /workspace

# Copiar los requirements e instalar dependencias de Python (base + desarrollo)
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt

# Exponer puertos
EXPOSE 8888

# Comando por defecto (docker-compose.yml no lo redefine)
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--IdentityProvider.token=", "--ServerApp.root_dir=/workspace", "--ServerApp.preferred_dir=/workspace"]