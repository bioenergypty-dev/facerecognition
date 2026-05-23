#!/bin/bash
# Script de inicio para Render

echo "🚀 Inicializando aplicación..."

echo "📦 Descargando modelos necesarios..."
python descargar_modelos.py

if [ $? -ne 0 ]; then
    echo "❌ Error al descargar modelos"
    exit 1
fi

echo "✅ Modelos descargados"
echo "🔧 Iniciando aplicación..."

python app.py
