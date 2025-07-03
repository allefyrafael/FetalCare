#!/bin/bash

# FetalCare Pro - Script de Inicialização
echo "🚀 FetalCare Pro - Sistema de Monitoramento Fetal"
echo "=================================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Instale o Docker Compose primeiro."
    exit 1
fi

echo "✅ Docker e Docker Compose encontrados"

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down 2>/dev/null

# Construir e iniciar serviços
echo "🔨 Construindo e iniciando serviços..."
docker-compose up --build -d

# Aguardar alguns segundos para os serviços iniciarem
echo "⏳ Aguardando serviços iniciarem..."
sleep 10

# Verificar status dos serviços
echo "🔍 Verificando status dos serviços..."

# Verificar backend
echo "Testando backend..."
if curl -s http://localhost:5000/ | grep -q "healthy"; then
    echo "✅ Backend está funcionando"
else
    echo "❌ Backend não está respondendo"
fi

# Verificar frontend
echo "Testando frontend..."
if curl -s http://localhost/health | grep -q "healthy"; then
    echo "✅ Frontend está funcionando"
else
    echo "❌ Frontend não está respondendo"
fi

echo ""
echo "🎉 Configuração concluída!"
echo ""
echo "📱 Acesse a aplicação em:"
echo "   Frontend: http://localhost"
echo "   API:      http://localhost:5000"
echo ""
echo "📝 Para ver logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Para parar:"
echo "   docker-compose down" 