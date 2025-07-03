# 🚀 Sistema FetalCare - Testes de Carga
## Estrutura Apache JMeter Profissional para Análise de Performance

---

## 🎯 **Visão Geral**

Este diretório contém a **suite completa de testes de carga** do Sistema FetalCare, implementada com **Apache JMeter** para análise profissional de performance. Os testes avaliam o comportamento do sistema sob diferentes condições de carga, focando em **tempo de resposta**, **taxa de erro** e **comportamento sob stress**.

### ✅ **Objetivos dos Testes**
- 📊 **Tempo de Resposta**: Medir latência em diferentes cenários
- ❌ **Taxa de Erro**: Avaliar estabilidade sob carga
- 🔥 **Comportamento sob Carga**: Stress testing e limites do sistema
- 📈 **Throughput**: Requisições por segundo suportadas
- 🧠 **Performance ML**: Comportamento do modelo sob carga

---

## 📁 **Estrutura dos Arquivos**

```
back-end/Testes/Carga/
├── 📋 README_JMETER.md              # Esta documentação
├── 🎯 plano_teste_fetalcare.jmx     # Plano principal JMeter
├── 📊 cenarios/                     # Cenários específicos
│   ├── stress_test.jmx              # Teste de stress
│   ├── load_test.jmx                # Teste de carga normal
│   ├── spike_test.jmx               # Teste de picos
│   └── endurance_test.jmx           # Teste de resistência
├── 📁 dados/                        # Dados de teste
│   ├── usuarios.csv                 # Dados de usuários
│   ├── gestantes.csv                # Dados de gestantes
│   └── parametros_ml.csv            # Parâmetros para ML
├── 📁 scripts/                      # Scripts auxiliares
│   ├── run_load_tests.py            # Executor automático
│   ├── generate_test_data.py        # Gerador de dados
│   └── analyze_results.py           # Analisador de resultados
├── 📁 resultados/                   # Resultados dos testes
│   ├── relatorios_html/             # Relatórios HTML
│   ├── logs/                        # Logs detalhados
│   └── graficos/                    # Gráficos de performance
├── 📁 configuracao/                 # Configurações
│   ├── jmeter.properties            # Propriedades JMeter
│   └── ambiente.properties          # Configurações de ambiente
└── 📊 RELATORIO_PERFORMANCE.md     # Relatório de resultados
```

---

## 🛠️ **Pré-requisitos e Instalação**

### 📥 **1. Instalação do Apache JMeter**
```bash
# Download JMeter (versão 5.6.3 ou superior)
# https://jmeter.apache.org/download_jmeter.cgi

# Windows
# Extrair para C:\apache-jmeter-5.6.3
# Adicionar C:\apache-jmeter-5.6.3\bin ao PATH

# Linux/Mac
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.zip
unzip apache-jmeter-5.6.3.zip
export PATH=$PATH:/path/to/apache-jmeter-5.6.3/bin
```

### 🐍 **2. Dependências Python**
```bash
pip install requests pandas matplotlib seaborn jinja2 xmltodict
```

### 🏥 **3. Sistema FetalCare Ativo**
```bash
# Garantir que o sistema esteja rodando
cd back-end
python app_with_database.py

# Verificar endpoints
curl http://localhost:5001/health
curl http://localhost:5001/api/gestantes
```

---

## 🎯 **Cenários de Teste Implementados**

### 📊 **1. Teste de Carga Normal (load_test.jmx)**
- **Objetivo**: Avaliar performance em condições normais
- **Usuários**: 50 usuários simultâneos
- **Duração**: 10 minutos
- **Ramp-up**: 2 minutos
- **Endpoints Testados**:
  - GET `/api/gestantes` (listagem)
  - POST `/api/exames` (criação de exames)
  - POST `/api/predict` (predições ML)

### 🔥 **2. Teste de Stress (stress_test.jmx)**
- **Objetivo**: Encontrar limites do sistema
- **Usuários**: 100 → 500 usuários (incremental)
- **Duração**: 20 minutos
- **Ramp-up**: 5 minutos
- **Critério de Falha**: Taxa de erro > 5%

### ⚡ **3. Teste de Picos (spike_test.jmx)**
- **Objetivo**: Avaliar comportamento em picos súbitos
- **Usuários**: 10 → 200 → 10 (pico súbito)
- **Duração**: 15 minutos
- **Padrão**: Carga normal com picos de 2 minutos

### 🏃 **4. Teste de Resistência (endurance_test.jmx)**
- **Objetivo**: Avaliar estabilidade em longo prazo
- **Usuários**: 30 usuários constantes
- **Duração**: 2 horas
- **Foco**: Memory leaks e degradação

---

## 📊 **Métricas Monitoradas**

### ⏱️ **Tempo de Resposta**
- **Tempo Médio**: Meta < 500ms
- **95º Percentil**: Meta < 1000ms
- **99º Percentil**: Meta < 2000ms
- **Tempo Máximo**: Meta < 5000ms

### ❌ **Taxa de Erro**
- **Taxa Geral**: Meta < 1%
- **Erros 4xx**: Erros de cliente
- **Erros 5xx**: Erros de servidor
- **Timeouts**: Meta < 0.5%

### 📈 **Throughput**
- **Requisições/seg**: Meta > 100 req/s
- **Bytes/seg**: Monitoramento de bandwidth
- **Transações/seg**: Operações completas

### 🧠 **Performance ML**
- **Tempo Predição**: Meta < 100ms
- **Throughput ML**: Meta > 50 predições/s
- **Accuracy sob Carga**: Manter > 95%

---

## 🚀 **Como Executar os Testes**

### 🎯 **Método 1: Script Automático (RECOMENDADO)**
```bash
# Executar todos os cenários
python scripts/run_load_tests.py --all

# Executar cenário específico
python scripts/run_load_tests.py --scenario load_test

# Com relatório automático
python scripts/run_load_tests.py --scenario stress_test --report
```

### 🔧 **Método 2: JMeter GUI**
```bash
# Abrir JMeter GUI
jmeter

# Carregar plano de teste
# File → Open → plano_teste_fetalcare.jmx

# Configurar Thread Groups
# Executar: Run → Start
```

### 💻 **Método 3: JMeter Command Line**
```bash
# Teste de carga básico
jmeter -n -t cenarios/load_test.jmx -l resultados/load_test_results.jtl

# Com relatório HTML
jmeter -n -t cenarios/stress_test.jmx -l resultados/stress_results.jtl -e -o resultados/relatorios_html/stress_report

# Teste completo
jmeter -n -t plano_teste_fetalcare.jmx -l resultados/complete_test.jtl -e -o resultados/relatorios_html/complete_report
```

---

## 📋 **Configuração dos Testes**

### 🎯 **Variáveis de Ambiente**
```properties
# ambiente.properties
HOST=localhost
PORT=5001
PROTOCOL=http
BASE_PATH=/api

# Configurações de carga
NORMAL_USERS=50
STRESS_USERS=500
SPIKE_USERS=200
ENDURANCE_USERS=30

# Timeouts
CONNECTION_TIMEOUT=5000
RESPONSE_TIMEOUT=10000
```

### ⚙️ **Propriedades JMeter**
```properties
# jmeter.properties
jmeter.save.saveservice.output_format=xml
jmeter.save.saveservice.response_data=false
jmeter.save.saveservice.samplerData=false
jmeter.save.saveservice.requestHeaders=false
jmeter.save.saveservice.responseHeaders=false

# Performance
jmeter.engine.nongui.maxport=4445
```

---

## 📊 **Análise de Resultados**

### 📈 **Métricas Principais**
```python
# Exemplo de análise automática
def analisar_resultados(arquivo_jtl):
    """
    Analisa resultados JMeter e gera relatório
    """
    metricas = {
        'tempo_resposta_medio': calcular_media(tempos),
        'percentil_95': calcular_percentil(tempos, 95),
        'taxa_erro': calcular_taxa_erro(resultados),
        'throughput': calcular_throughput(resultados),
        'disponibilidade': calcular_disponibilidade(resultados)
    }
    return metricas
```

### 🎯 **Critérios de Aprovação**
| Métrica | Meta | Crítico |
|---------|------|---------|
| **Tempo Resposta Médio** | < 500ms | < 1000ms |
| **95º Percentil** | < 1000ms | < 2000ms |
| **Taxa de Erro** | < 1% | < 5% |
| **Throughput** | > 100 req/s | > 50 req/s |
| **Disponibilidade** | > 99.5% | > 99% |

---

## 🔍 **Monitoramento Durante Testes**

### 📊 **Métricas do Sistema**
```bash
# Monitoramento de recursos
htop              # CPU e Memória
iotop             # I/O de disco
netstat -i        # Tráfego de rede
df -h             # Espaço em disco
```

### 🐍 **Monitoramento da API**
```python
# Script de monitoramento em tempo real
import requests
import time

def monitorar_api():
    while True:
        try:
            response = requests.get('http://localhost:5001/health')
            print(f"Status: {response.status_code}, Tempo: {response.elapsed.total_seconds():.3f}s")
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(5)
```

### 🧠 **Monitoramento ML**
```python
# Monitoramento específico do modelo ML
def monitorar_ml():
    """Monitor performance do modelo ML sob carga"""
    tempos_predicao = []
    acuracia_amostras = []
    
    # Coletar métricas durante teste
    # Gerar relatório de performance ML
```

---

## 📋 **Cenários de Teste Detalhados**

### 🎯 **Cenário 1: Operações CRUD**
```xml
<!-- Exemplo de Thread Group para CRUD -->
<ThreadGroup>
    <stringProp name="ThreadGroup.num_threads">50</stringProp>
    <stringProp name="ThreadGroup.ramp_time">120</stringProp>
    <stringProp name="ThreadGroup.duration">600</stringProp>
    
    <!-- Criar Gestante -->
    <HTTPSamplerProxy>
        <stringProp name="HTTPSampler.path">/api/gestantes</stringProp>
        <stringProp name="HTTPSampler.method">POST</stringProp>
    </HTTPSamplerProxy>
    
    <!-- Listar Gestantes -->
    <HTTPSamplerProxy>
        <stringProp name="HTTPSampler.path">/api/gestantes</stringProp>
        <stringProp name="HTTPSampler.method">GET</stringProp>
    </HTTPSamplerProxy>
</ThreadGroup>
```

### 🤖 **Cenário 2: Predições ML**
```xml
<!-- Thread Group específico para ML -->
<ThreadGroup>
    <stringProp name="ThreadGroup.num_threads">30</stringProp>
    
    <!-- Predição ML -->
    <HTTPSamplerProxy>
        <stringProp name="HTTPSampler.path">/api/predict</stringProp>
        <stringProp name="HTTPSampler.method">POST</stringProp>
        <elementProp name="HTTPsampler.Arguments">
            <Arguments>
                <Argument name="baseline_value">140</Argument>
                <Argument name="accelerations">3</Argument>
                <!-- ... outros parâmetros -->
            </Arguments>
        </elementProp>
    </HTTPSamplerProxy>
</ThreadGroup>
```

---

## 🛠️ **Scripts Auxiliares**

### 🎯 **Gerador de Dados de Teste**
```python
# generate_test_data.py
import csv
import random
from faker import Faker

def gerar_dados_gestantes(quantidade=1000):
    """Gera dados de teste para gestantes"""
    fake = Faker('pt_BR')
    
    with open('dados/gestantes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['patient_id', 'patient_name', 'patient_cpf', 'gestational_age'])
        
        for i in range(quantidade):
            writer.writerow([
                f'TEST{i:04d}',
                fake.name(),
                fake.cpf(),
                random.randint(20, 40)
            ])

def gerar_parametros_ml(quantidade=5000):
    """Gera parâmetros para testes ML"""
    # Implementar geração de 21 features realistas
    pass
```

### 📊 **Executor Automático**
```python
# run_load_tests.py
import subprocess
import argparse
import datetime
import os

def executar_teste_jmeter(cenario, relatorio=True):
    """
    Executa teste JMeter e gera relatórios
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    resultado_file = f'resultados/{cenario}_{timestamp}.jtl'
    relatorio_dir = f'resultados/relatorios_html/{cenario}_{timestamp}'
    
    # Comando JMeter
    cmd = [
        'jmeter',
        '-n',
        '-t', f'cenarios/{cenario}.jmx',
        '-l', resultado_file
    ]
    
    if relatorio:
        cmd.extend(['-e', '-o', relatorio_dir])
    
    # Executar
    print(f"🚀 Executando teste: {cenario}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Teste concluído: {cenario}")
        if relatorio:
            print(f"📊 Relatório: {relatorio_dir}/index.html")
    else:
        print(f"❌ Erro no teste: {result.stderr}")
    
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description='Executor de Testes de Carga')
    parser.add_argument('--scenario', choices=['load_test', 'stress_test', 'spike_test', 'endurance_test', 'all'])
    parser.add_argument('--report', action='store_true', help='Gerar relatório HTML')
    
    args = parser.parse_args()
    
    if args.scenario == 'all':
        cenarios = ['load_test', 'stress_test', 'spike_test']
    else:
        cenarios = [args.scenario]
    
    for cenario in cenarios:
        executar_teste_jmeter(cenario, args.report)

if __name__ == '__main__':
    main()
```

---

## 📊 **Interpretação de Resultados**

### 📈 **Gráficos Importantes**
1. **Response Time Over Time**: Tendência de tempo de resposta
2. **Throughput vs Users**: Relação carga vs throughput
3. **Error Rate**: Taxa de erro ao longo do tempo
4. **Resource Utilization**: Uso de CPU/Memória

### 🎯 **Indicadores de Performance**
```python
def avaliar_performance(resultados):
    """
    Avalia se o sistema passou nos testes
    """
    criterios = {
        'tempo_resposta_ok': resultados['tempo_medio'] < 500,
        'percentil_95_ok': resultados['percentil_95'] < 1000,
        'taxa_erro_ok': resultados['taxa_erro'] < 0.01,
        'throughput_ok': resultados['throughput'] > 100,
        'disponibilidade_ok': resultados['disponibilidade'] > 0.995
    }
    
    aprovado = all(criterios.values())
    return aprovado, criterios
```

---

## 🔄 **Integração com CI/CD**

### 🚀 **GitHub Actions**
```yaml
name: Load Tests
on:
  schedule:
    - cron: '0 2 * * 1'  # Segunda-feira às 2h

jobs:
  load-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup JMeter
        run: |
          wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.zip
          unzip apache-jmeter-5.6.3.zip
          export PATH=$PATH:$PWD/apache-jmeter-5.6.3/bin
      
      - name: Start FetalCare System
        run: |
          cd back-end
          python app_with_database.py &
          sleep 30
      
      - name: Run Load Tests
        run: |
          cd back-end/Testes/Carga
          python scripts/run_load_tests.py --scenario load_test --report
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: load-test-results
          path: back-end/Testes/Carga/resultados/
```

---

## 🎯 **Melhores Práticas**

### ✅ **Preparação dos Testes**
1. **Ambiente Isolado**: Usar ambiente dedicado para testes
2. **Dados Realistas**: Usar dados similares à produção
3. **Monitoramento**: Monitorar recursos durante testes
4. **Baseline**: Estabelecer baseline antes de mudanças

### 📊 **Durante a Execução**
1. **Warm-up**: Permitir aquecimento do sistema
2. **Ramp-up Gradual**: Aumentar carga gradualmente
3. **Monitoramento Ativo**: Acompanhar métricas em tempo real
4. **Logs Detalhados**: Manter logs para análise posterior

### 🔍 **Análise de Resultados**
1. **Múltiplas Execuções**: Executar testes múltiplas vezes
2. **Análise Estatística**: Usar médias e percentis
3. **Correlação**: Correlacionar métricas de aplicação e sistema
4. **Documentação**: Documentar achados e recomendações

---

## 🏆 **Conclusão**

Esta estrutura de testes de carga com **Apache JMeter** fornece uma base sólida para avaliar a performance do Sistema FetalCare. Os testes cobrem cenários realistas e fornecem métricas detalhadas para garantir que o sistema possa suportar a carga esperada em produção.

### 🎯 **Próximos Passos**
1. **Implementar Cenários**: Criar arquivos .jmx específicos
2. **Configurar Monitoramento**: Setup de métricas detalhadas
3. **Automatizar Execução**: Scripts para execução regular
4. **Integrar CI/CD**: Testes automáticos em pipeline

---

**📅 Última Atualização**: 03/07/2025  
**🔬 Responsável**: Sistema de Testes de Performance  
**📊 Versão**: Apache JMeter 5.6.3  
**🏥 Sistema**: FetalCare - Monitoramento Fetal Inteligente 