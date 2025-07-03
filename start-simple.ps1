# FetalCare Pro - Script Simples de Inicialização
Write-Host "FetalCare Pro - Sistema de Monitoramento Fetal" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

Write-Host "Verificando Docker..." -ForegroundColor Yellow
docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Docker não encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "Verificando Docker Compose..." -ForegroundColor Yellow
docker-compose --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Docker Compose não encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "Parando containers existentes..." -ForegroundColor Yellow
docker-compose down

Write-Host "Construindo e iniciando serviços..." -ForegroundColor Yellow
docker-compose up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha ao iniciar containers" -ForegroundColor Red
    exit 1
}

Write-Host "Aguardando serviços iniciarem..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

Write-Host "Verificando containers..." -ForegroundColor Yellow
docker-compose ps

Write-Host "Testando backend..." -ForegroundColor Yellow
for ($i = 1; $i -le 5; $i++) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5000/" -TimeoutSec 5
        if ($response.status -eq "healthy") {
            Write-Host "SUCESSO: Backend funcionando!" -ForegroundColor Green
            Write-Host "   Modelo carregado: $($response.model_loaded)" -ForegroundColor White
            break
        }
    }
    catch {
        Write-Host "Tentativa $i/5..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
    }
}

Write-Host ""
Write-Host "SISTEMA INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "Frontend: http://localhost" -ForegroundColor Cyan
Write-Host "API: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Comandos úteis:" -ForegroundColor Yellow
Write-Host "   docker-compose logs -f    # Ver logs" -ForegroundColor White
Write-Host "   docker-compose down       # Parar" -ForegroundColor White
Write-Host "   .\test-api.ps1           # Testar API" -ForegroundColor White

$openBrowser = Read-Host "Abrir navegador? (y/n)"
if ($openBrowser -eq "y") {
    Start-Process "http://localhost"
} 