#!/bin/bash
set -e

echo "🚀 Iniciando entorno de Ingeniería de Datos"
echo "==========================================="

# Configurar git si no existe
if [ ! -f ~/.gitconfig ]; then
    echo "⚙️ Configurando Git..."
    git config --global init.defaultBranch main
    git config --global core.editor "vim"
fi

# Verificar instalaciones
echo "📦 Versiones instaladas:"
python --version
pip --version
git --version
java --version
spark-submit --version 2>/dev/null || echo "Spark disponible"

# Crear directorios necesarios
mkdir -p /workspace/{notebooks,scripts,data,projects}

# Mostrar ayuda
echo ""
echo "✅ Entorno listo!"
echo "📓 Accede a Jupyter Lab: http://localhost:8888"
echo "🔗 PostgreSQL: jdbc:postgresql://postgres:5432/dataengineering"
echo "🔗 MongoDB: mongodb://datacourse:datacourse123@mongodb:27017"
echo "🔗 Redis: redis://redis:6379"
echo ""

# Ejecutar el comando recibido
exec "$@"