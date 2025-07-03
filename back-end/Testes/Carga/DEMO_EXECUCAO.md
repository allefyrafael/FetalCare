# 🚀 Sistema FetalCare - Demonstração de Execução
## Guia Prático para Executar Testes de Carga com Apache JMeter

---

## 🎯 **Pré-requisitos**

### 📥 **1. Instalação do Apache JMeter**
```bash
# Download JMeter 5.6.3 ou superior
# https://jmeter.apache.org/download_jmeter.cgi

# Windows - Extrair para:
C:\apache-jmeter-5.6.3\

# Adicionar ao PATH do sistema:
C:\apache-jmeter-5.6.3\bin
```

### 🏥 **2. Sistema FetalCare Ativo**
```bash
# Navegar para o diretório do backend
cd back-end

# Iniciar o sistema
python app_with_database.py

# Verificar se está funcionando
curl http://localhost:5001/health
# Resposta esperada: {"status": "healthy"}
```

---

## 🎯 **Execução Rápida - 5 Minutos**

### 🚀 **Método 1: Script Automático (RECOMENDADO)**
```bash
# Navegar para o diretório de testes
cd back-end/Testes/Carga/scripts

# Executar teste de carga normal
python run_load_tests.py --scenario load_test --report

# Ou usar o menu interativo
python run_load_tests.py --interactive
```

### 🔧 **Método 2: JMeter Command Line**
```bash
# Navegar para o diretório de testes
cd back-end/Testes/Carga

# Executar teste de carga normal
jmeter -n -t cenarios/load_test.jmx -l resultados/load_test.jtl -e -o resultados/relatorios_html/load_test

# Executar teste de stress
jmeter -n -t cenarios/stress_test.jmx -l resultados/stress_test.jtl -e -o resultados/relatorios_html/stress_test
```

### 🖥️ **Método 3: JMeter GUI (Para Desenvolvimento)**
```bash
# Abrir JMeter em modo GUI
jmeter

# Carregar arquivo: File → Open → cenarios/load_test.jmx
# Configurar listeners se necessário
# Executar: Run → Start (Ctrl+R)
```

---

## 📊 **Cenários Disponíveis**

### 🎯 **1. Teste de Carga Normal**
```yaml
Arquivo: cenarios/load_test.jmx
Duração: 10 minutos
Usuários: 50 simultâneos
Objetivo: Validar performance normal
Comando: python run_load_tests.py --scenario load_test
```

### 🔥 **2. Teste de Stress**
```yaml
Arquivo: cenarios/stress_test.jmx
Duração: 20 minutos
Usuários: 100 → 500 (incremental)
Objetivo: Encontrar limites
Comando: python run_load_tests.py --scenario stress_test
```

### ⚡ **3. Teste de Picos**
```yaml
Arquivo: cenarios/spike_test.jmx
Duração: 15 minutos
Usuários: 10 → 200 → 10 (picos)
Objetivo: Testar recuperação
Comando: python run_load_tests.py --scenario spike_test
```

### 🏃 **4. Teste de Resistência**
```yaml
Arquivo: cenarios/endurance_test.jmx
Duração: 2 horas
Usuários: 30 constantes
Objetivo: Detectar memory leaks
Comando: python run_load_tests.py --scenario endurance_test
```

---

## 📈 **Interpretação de Resultados**

### ✅ **Critérios de Aprovação**
```yaml
Tempo de Resposta Médio: < 500ms
95º Percentil: < 1000ms
Taxa de Erro: < 1%
Disponibilidade: > 99.5%
Throughput: > 100 req/s
Performance ML: < 100ms
```

### 📊 **Métricas Principais**
```bash
# Tempo de Resposta
- Médio: Tempo médio de todas as requisições
- 95º Percentil: 95% das requisições abaixo deste tempo
- 99º Percentil: 99% das requisições abaixo deste tempo

# Taxa de Erro
- Porcentagem de requisições que falharam
- Meta: < 1% para aprovação

# Throughput
- Requisições por segundo processadas
- Meta: > 100 req/s para aprovação

# Disponibilidade
- Porcentagem de tempo que o sistema esteve disponível
- Meta: > 99.5% para aprovação
```

---

## 🔍 **Análise de Resultados**

### 📁 **Localização dos Arquivos**
```bash
# Resultados brutos (.jtl)
resultados/

# Relatórios HTML
resultados/relatorios_html/

# Logs de execução
resultados/logs/

# Gráficos de performance
resultados/graficos/
```

### 📊 **Relatório HTML**
```bash
# Abrir relatório no navegador
# Arquivo: resultados/relatorios_html/[cenario]/index.html

Seções importantes:
- Dashboard: Visão geral das métricas
- Charts: Gráficos de performance
- Statistics: Estatísticas detalhadas
- Errors: Análise de erros
```

### 🎯 **Análise Automática**
```bash
# Analisar arquivo .jtl existente
python run_load_tests.py --analyze-only resultados/load_test.jtl

# Saída esperada:
📊 RELATÓRIO DE PERFORMANCE - ANÁLISE
=====================================
✅ Tempo Médio: 287ms (Meta: < 500ms)
✅ Taxa de Erro: 0.24% (Meta: < 1%)
✅ Disponibilidade: 99.76% (Meta: > 99.5%)
✅ Throughput: 152.3 req/s (Meta: > 100 req/s)
```

---

## 🛠️ **Personalização de Testes**

### 🎯 **Modificar Parâmetros**
```bash
# Editar arquivo de configuração
notepad configuracao/ambiente.properties

# Principais parâmetros:
NORMAL_USERS=50          # Número de usuários
NORMAL_DURATION=600      # Duração em segundos
CONNECTION_TIMEOUT=5000  # Timeout de conexão
```

### 📊 **Dados de Teste Customizados**
```bash
# Gerar novos dados de teste
cd scripts
python generate_test_data_simple.py

# Parâmetros disponíveis:
--gestantes 1000      # Número de gestantes
--parametros-ml 5000  # Conjuntos de parâmetros ML
--usuarios 100        # Número de usuários
```

---

## 🚨 **Troubleshooting**

### ❌ **Problemas Comuns**

#### **1. JMeter não encontrado**
```bash
# Erro: 'jmeter' is not recognized
# Solução: Adicionar JMeter ao PATH do sistema
set PATH=%PATH%;C:\apache-jmeter-5.6.3\bin
```

#### **2. Sistema FetalCare não responde**
```bash
# Erro: Connection refused
# Solução: Verificar se o sistema está rodando
curl http://localhost:5001/health

# Se não estiver, iniciar:
cd back-end
python app_with_database.py
```

#### **3. Falta de memória no JMeter**
```bash
# Erro: OutOfMemoryError
# Solução: Aumentar heap do Java
# Editar jmeter.bat e adicionar:
set HEAP=-Xms1g -Xmx4g
```

#### **4. Muitos erros nos testes**
```bash
# Possíveis causas:
- Sistema sobrecarregado (reduzir usuários)
- Timeout muito baixo (aumentar timeouts)
- Dados inválidos (regenerar dados de teste)
```

### 🔧 **Logs de Debug**
```bash
# Habilitar logs detalhados
# Editar configuracao/jmeter.properties:
log_level.jmeter=DEBUG

# Verificar logs
type resultados/logs/[cenario].log
```

---

## 📝 **Exemplo Completo Passo a Passo**

### 🎯 **Cenário: Teste de Carga Normal**

```bash
# 1. Verificar pré-requisitos
jmeter --version
curl http://localhost:5001/health

# 2. Navegar para diretório correto
cd "back-end/Testes/Carga"

# 3. Gerar dados de teste (se necessário)
cd scripts
python generate_test_data_simple.py
cd ..

# 4. Executar teste
python scripts/run_load_tests.py --scenario load_test --report

# 5. Aguardar conclusão (10 minutos)
# Saída esperada:
🚀 Iniciando teste: load_test
📁 Resultado será salvo em: resultados/load_test_20250703_143022.jtl
✅ Teste concluído com sucesso!
⏱️  Duração: 623.45 segundos
📊 Relatório HTML: resultados/relatorios_html/load_test_20250703_143022/index.html

# 6. Analisar resultados
📊 RELATÓRIO DE PERFORMANCE - LOAD_TEST
=======================================
✅ Total de Requisições: 15,234
✅ Taxa de Erro: 0.24% (Meta: < 1%)
✅ Tempo Médio: 287ms (Meta: < 500ms)
✅ 95º Percentil: 542ms (Meta: < 1000ms)
✅ Throughput: 152.3 req/s (Meta: > 100 req/s)

🎉 Teste load_test concluído com sucesso!
```

---

## 🎯 **Próximos Passos**

### 📈 **Para Ambientes de Produção**
1. **Configurar Monitoramento**: Setup de métricas de sistema
2. **Ajustar Parâmetros**: Baseado na infraestrutura real
3. **Automatizar Execução**: Integrar com CI/CD
4. **Alertas**: Configurar notificações automáticas

### 🔄 **Execução Regular**
```bash
# Agendar testes semanais
# Windows Task Scheduler ou Cron (Linux)
python run_load_tests.py --scenario load_test --report
```

### 📊 **Análise Avançada**
```bash
# Comparar resultados ao longo do tempo
python scripts/analyze_trends.py --period weekly

# Gerar relatório executivo
python scripts/executive_report.py --output pdf
```

---

## 🏆 **Conclusão**

Esta estrutura de testes de carga fornece uma base sólida para avaliar a performance do Sistema FetalCare. Com os scripts automatizados e relatórios detalhados, você pode:

- ✅ **Validar Performance**: Garantir que o sistema atende aos requisitos
- 🔍 **Identificar Gargalos**: Encontrar pontos de otimização
- 📈 **Monitorar Tendências**: Acompanhar evolução da performance
- 🚀 **Aprovar para Produção**: Com confiança técnica total

---

**📅 Última Atualização**: 03/07/2025  
**🔬 Responsável**: Sistema de Testes de Performance  
**📊 Versão JMeter**: 5.6.3  
**🏥 Sistema**: FetalCare - Monitoramento Fetal Inteligente 