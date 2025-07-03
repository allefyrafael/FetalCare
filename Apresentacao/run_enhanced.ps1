# Script para executar a aplicação FetalCare Enhanced
Write-Host "🏥 Iniciando FetalCare Enhanced Dashboard..." -ForegroundColor Green

# Verificar se streamlit está instalado
try {
    streamlit --version | Out-Null
    Write-Host "✅ Streamlit encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ Streamlit não encontrado. Instalando..." -ForegroundColor Red
    pip install streamlit
}

# Verificar dependências
$dependencies = @("plotly", "pandas", "numpy")
foreach ($dep in $dependencies) {
    try {
        python -c "import $dep" 2>$null
        Write-Host "✅ $dep disponível" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Instalando $dep..." -ForegroundColor Yellow
        pip install $dep
    }
}

Write-Host ""
Write-Host "🚀 Iniciando Dashboard FetalCare Enhanced..." -ForegroundColor Cyan
Write-Host "📊 Acesse: http://localhost:8502" -ForegroundColor Yellow
Write-Host "🔧 Para parar: Ctrl+C" -ForegroundColor Gray
Write-Host ""

# Executar aplicação
streamlit run app_fetalcare_enhanced.py --server.port 8502 