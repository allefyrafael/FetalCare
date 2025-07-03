# 📋 Testes E2E (End-to-End) - Sistema FetalCare

## 📝 Índice

1. [🎯 Visão Geral](#-visão-geral)
2. [🔧 Pré-requisitos](#-pré-requisitos)
3. [📦 Instalação](#-instalação)
4. [🏗️ Estrutura dos Testes](#️-estrutura-dos-testes)
5. [🧪 Cenários de Teste](#-cenários-de-teste)
6. [🚀 Execução dos Testes](#-execução-dos-testes)
7. [📊 Relatórios](#-relatórios)
8. [🔍 Debugging](#-debugging)
9. [📝 Guias de Contribuição](#-guias-de-contribuição)

---

## 🎯 Visão Geral

### Objetivo
Os testes E2E (End-to-End) do sistema FetalCare validam o **fluxo completo** da aplicação do ponto de vista do usuário, simulando interações reais com o frontend e verificando se todas as funcionalidades funcionam corretamente em conjunto.

### Tecnologias Utilizadas
- **Selenium WebDriver** com Python
- **ChromeDriver** (gerenciado automaticamente)
- **pytest** como framework de testes
- **Allure** para relatórios visuais
- **Page Object Model** para manutenibilidade

### Cobertura dos Testes
- ✅ **Preenchimento de formulários** (gestante + monitoramento)
- ✅ **Análise de Machine Learning** (21 parâmetros)
- ✅ **Visualização de resultados** (classificação + recomendações)
- ✅ **Navegação entre páginas** (home → registros)
- ✅ **Validações de entrada** (campos obrigatórios)
- ✅ **Responsividade** (desktop, tablet, mobile)
- ✅ **Performance** (critérios de tempo)
- ✅ **Tratamento de erros** (dados inválidos)

---

## 🔧 Pré-requisitos

### Sistema Operacional
- Windows, macOS ou Linux
- Python 3.8 ou superior

### Software Necessário
```bash
# Python e pip
python --version  # 3.8+
pip --version

# Google Chrome (versão atual)
# O ChromeDriver é gerenciado automaticamente
```

### Serviços do FetalCare
```bash
# Frontend (obrigatório)
http://localhost:8080

# API Backend (obrigatório)  
http://localhost:5001

# MongoDB (verificação automática)
mongodb://localhost:27017
```

### Verificação Rápida
```bash
# Testar conectividade
curl http://localhost:8080
curl http://localhost:5001/health
```

---

## 📦 Instalação

### 1. Navegação
```bash
cd back-end/Testes/E2E
```

### 2. Dependências Python
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Ou instalação individual
pip install selenium==4.15.2
pip install pytest==7.4.3
pip install webdriver-manager==4.0.1
pip install allure-pytest==2.13.2
pip install colorama==0.4.6
```

### 3. Configuração do ChromeDriver (Automática)
```bash
# O webdriver-manager baixa automaticamente a versão correta
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

### 4. Verificação da Instalação
```bash
# Testar pytest
pytest --version

# Testar Selenium
python -c "from selenium import webdriver; print('Selenium OK')"

# Testar configuração completa
python scripts/run_e2e_tests.py
```

---

## 🏗️ Estrutura dos Testes

### 📁 Arquitetura Completa
```
E2E/
├── 📋 README_E2E.md              # Esta documentação
├── ⚙️ pytest.ini                # Configurações do pytest
├── 🔧 conftest.py               # Fixtures compartilhadas
├── 📦 requirements.txt          # Dependências Python
├── 📊 RELATORIO_E2E.md          # Relatório de implementação
├── 🚀 DEMO_EXECUCAO_E2E.md      # Guia de demonstração
│
├── 📁 cenarios/                 # Cenários de teste
│   ├── test_fluxo_completo.py   # Fluxo principal E2E
│   ├── test_formulario_gestante.py
│   ├── test_monitoramento.py
│   ├── test_analise_ml.py
│   ├── test_navegacao.py
│   ├── test_registros.py
│   ├── test_validacoes.py
│   └── test_responsividade.py
│
├── 📁 page_objects/             # Page Object Model
│   ├── base_page.py             # Classe base (500+ linhas)
│   ├── home_page.py             # Página principal (800+ linhas)
│   ├── records_page.py          # Página de registros
│   └── components/              # Componentes reutilizáveis
│       ├── form_gestante.py
│       ├── form_monitoramento.py
│       └── results_display.py
│
├── 📁 scripts/                  # Scripts auxiliares
│   ├── run_e2e_tests.py         # Executor principal (600+ linhas)
│   ├── setup_chromedriver.py   # Configuração WebDriver
│   ├── generate_test_data.py    # Gerador de dados
│   └── report_generator.py     # Gerador de relatórios
│
├── 📁 dados/                    # Dados de teste
│   ├── gestantes_validas.json   # 70+ casos de gestantes
│   ├── parametros_ml.json       # 12 cenários ML
│   ├── casos_extremos.json      # Casos limite
│   └── casos_invalidos.json     # Dados inválidos
│
├── 📁 configuracao/             # Configurações
│   ├── ambiente.properties      # URLs e configurações
│   ├── selenium.properties      # Config Selenium
│   └── timeouts.json           # Timeouts personalizados
│
├── 📁 evidencias/              # Evidências de execução
│   ├── screenshots/            # Capturas de tela
│   └── logs/                   # Logs detalhados
│
└── 📁 relatorios/              # Relatórios
    ├── allure-results/         # Dados para Allure
    ├── allure-report/          # Relatório Allure gerado
    ├── html/                   # Relatórios HTML
    └── junit/                  # XML para CI/CD
```

### 🎭 Page Object Model

#### **BasePage** (Classe Fundamental)
```python
# Funcionalidades principais:
- aguardar_elemento()          # Explicit waits
- clicar()                     # Cliques seguros
- digitar()                    # Entrada de texto
- obter_texto()               # Extração de dados
- obter_screenshot()          # Evidências
- aguardar_loading_desaparecer() # Performance
```

#### **HomePage** (Página Principal)
```python
# Elementos mapeados:
- Formulário de gestante (5 campos)
- Formulário de monitoramento (21 parâmetros)
- Seção de resultados
- Botões de ação
- Status de conexão

# Métodos principais:
- preencher_dados_gestante()
- preencher_parametros_monitoramento()
- realizar_analise_fetal()
- obter_resultado_analise()
- aguardar_resultados_aparecerem()
```

---

## 🧪 Cenários de Teste

### 1. 🎯 **Fluxo Completo** (test_fluxo_completo.py)

#### **test_fluxo_completo_normal**
```python
@pytest.mark.critical
@pytest.mark.regression
@pytest.mark.smoke
```
- ✅ Preenchimento de gestante
- ✅ Preenchimento de monitoramento  
- ✅ Execução de análise ML
- ✅ Verificação de resultados
- ✅ Salvamento de dados
- ✅ Navegação para registros

#### **test_fluxo_completo_risco**
```python
@pytest.mark.critical
@pytest.mark.ml
```
- ⚠️ Parâmetros indicando risco fetal
- ⚠️ Validação de classificação "RISCO"
- ⚠️ Verificação de recomendações específicas

#### **test_performance_fluxo_completo**
```python
@pytest.mark.performance
@pytest.mark.fast
```
- ⏱️ Análise ML < 10 segundos
- ⏱️ Fluxo completo < 30 segundos
- ⏱️ Carregamento página < 5 segundos

### 2. 📝 **Formulários** (test_formulario_gestante.py)

#### Validações Implementadas:
- **Campos obrigatórios**: Nome, ID, Idade Gestacional
- **Campos opcionais**: CPF, Idade Materna
- **Validação de CPF**: Formato e dígitos verificadores
- **Limites de idade**: Gestacional (1-42 semanas)
- **Caracteres especiais**: Nomes internacionais

### 3. 🤖 **Análise ML** (test_analise_ml.py)

#### Cenários de Machine Learning:
- **Normal**: 140 bpm, 3 acelerações, movimento normal
- **Risco Leve**: 160 bpm, taquicardia leve
- **Risco Moderado**: 175 bpm, múltiplos indicadores
- **Crítico**: 190 bpm, emergência obstétrica
- **Bradicardia**: 100 bpm, frequência baixa
- **Variabilidade Ausente**: Padrão sinusoidal

### 4. 🔍 **Validações** (test_validacoes.py)

#### Tipos de Validação:
- **Frontend**: JavaScript validation
- **Backend**: Server-side validation
- **Formato**: CPF, números, texto
- **Obrigatoriedade**: Campos essenciais
- **Limites**: Min/max values

### 5. 📱 **Responsividade** (test_responsividade.py)

#### Resoluções Testadas:
- **Desktop**: 1920x1080 (layout completo)
- **Tablet**: 768x1024 (layout adaptado)
- **Mobile**: 375x667 (layout responsivo)

---

## 🚀 Execução dos Testes

### 🎮 Executor Interativo (Recomendado)

```bash
# Iniciar menu interativo
python scripts/run_e2e_tests.py
```

**Menu principal:**
```
📋 MENU PRINCIPAL
──────────────────────────────────────────────────
  1 - 🎯 Executar Fluxo Completo
  2 - 📝 Executar Testes de Formulário
  3 - 🤖 Executar Testes de Análise ML
  4 - 🔍 Executar Testes de Validação
  5 - 📱 Executar Testes de Responsividade
  6 - 🚀 Executar TODOS os Testes
  7 - 📊 Gerar Relatório
  8 - 🔧 Configurações
  9 - ❓ Ajuda
  0 - 🚪 Sair
──────────────────────────────────────────────────
```

### ⚡ Execução Rápida (Linha de Comando)

#### Comandos Básicos:
```bash
# Fluxo completo apenas
pytest cenarios/test_fluxo_completo.py -v

# Testes críticos
pytest -m critical -v

# Testes de fumaça (smoke)
pytest -m smoke --headless

# Todos os testes
pytest cenarios/ -v
```

#### Comandos Avançados:
```bash
# Execução paralela
pytest -n auto

# Com timeout personalizado  
pytest --timeout=60

# Modo headless (sem interface)
pytest --headless

# Screenshots sempre
pytest --capture-screenshots

# Browser específico
pytest --browser=firefox

# URL customizada
pytest --base-url=http://staging.fetalcare.com
```

### 🔧 Configurações Personalizadas

#### Via Interface:
```bash
python scripts/run_e2e_tests.py
# Escolher opção 8 - 🔧 Configurações
```

#### Via Linha de Comando:
```bash
# Configuração completa
pytest cenarios/test_fluxo_completo.py \
  --headless \
  --capture-screenshots \
  --timeout=300 \
  --alluredir=relatorios/allure-results \
  --html=relatorios/html/report.html \
  --self-contained-html
```

### 📊 Execução com Marcadores

```bash
# Por categoria
pytest -m "critical"           # Testes críticos
pytest -m "smoke"             # Testes básicos
pytest -m "regression"        # Testes de regressão
pytest -m "ml"                # Machine Learning
pytest -m "performance"       # Performance
pytest -m "mobile"            # Responsividade

# Combinações
pytest -m "critical and not slow"
pytest -m "smoke or regression"
pytest -m "ml and performance"
```

---

## 📊 Relatórios

### 📈 Allure Reports (Recomendado)

#### Geração Automática:
```bash
# Via menu interativo
python scripts/run_e2e_tests.py
# Escolher: 7 - 📊 Gerar Relatório
```

#### Geração Manual:
```bash
# Executar testes com Allure
pytest --alluredir=relatorios/allure-results

# Gerar relatório
allure generate relatorios/allure-results -o relatorios/allure-report --clean

# Abrir no navegador
allure open relatorios/allure-report
```

#### Conteúdo do Allure:
- 📊 **Dashboard**: Estatísticas gerais
- 📈 **Gráficos**: Timeline, tendências
- 📝 **Detalhes**: Passos de cada teste
- 🖼️ **Screenshots**: Evidências visuais
- ⏱️ **Performance**: Métricas de tempo
- 📋 **Histórico**: Execuções anteriores

### 📄 Relatório HTML

```bash
# Gerar relatório HTML simples
pytest --html=relatorios/html/report.html --self-contained-html

# Abrir relatório
# Windows
start relatorios/html/report.html

# Linux/Mac
open relatorios/html/report.html
```

### 📊 Relatório JUnit (CI/CD)

```bash
# Gerar XML para Jenkins/GitLab
pytest --junitxml=relatorios/junit/results.xml
```

### 📸 Screenshots e Evidências

#### Captura Automática:
- ❌ **Falhas**: Screenshot + HTML da página
- ✅ **Marcos**: Screenshots em pontos importantes
- 🔍 **Debug**: Logs detalhados

#### Localização:
```
evidencias/
├── screenshots/
│   ├── test_fluxo_completo_falha_20241219_143022.png
│   ├── test_fluxo_completo_01_estado_inicial.png
│   └── test_fluxo_completo_06_resultados_exibidos.png
└── logs/
    ├── pytest.log
    └── selenium.log
```

---

## 🔍 Debugging

### 🐛 Debugging Interativo

#### Execução com Pausa:
```bash
# Parar em falhas
pytest cenarios/test_fluxo_completo.py --pdb

# Logs verbosos
pytest cenarios/test_fluxo_completo.py -v -s --log-cli-level=DEBUG
```

#### Debugging no Código:
```python
# Adicionar breakpoint
import pdb; pdb.set_trace()

# Pausa para inspeção visual
import time; time.sleep(10)

# Screenshot manual
self.home_page.obter_screenshot("debug_ponto_especifico")
```

### 📋 Log Levels

#### Configuração de Logs:
```python
# conftest.py já configurado com:
log_cli = true
log_cli_level = INFO
log_file = evidencias/logs/pytest.log
```

#### Logs Disponíveis:
- **INFO**: Ações principais
- **DEBUG**: Detalhes técnicos
- **WARNING**: Alertas
- **ERROR**: Erros capturados

### 🔧 Solução de Problemas

#### ChromeDriver:
```bash
# Reinstalar ChromeDriver
pip install --upgrade webdriver-manager
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

#### Timeouts:
```bash
# Aumentar timeouts para debugging
pytest --timeout=300
```

#### Elementos não encontrados:
```python
# Usar waits mais longos
self.aguardar_elemento(localizador, timeout=30)
```

#### Performance lenta:
```bash
# Usar modo headless
pytest --headless

# Reduzir logs
pytest --log-cli-level=WARNING
```

---

## 📝 Guias de Contribuição

### 🔨 Criando Novos Testes

#### 1. Estrutura Básica:
```python
import pytest
import allure
from ..page_objects.home_page import HomePage

@allure.epic("FetalCare E2E")
@allure.feature("Nova Funcionalidade")
class TestNovaFuncionalidade:
    
    @pytest.fixture(autouse=True)
    def setup(self, navegador):
        self.driver = navegador
        self.home_page = HomePage(self.driver)
    
    @allure.story("Cenário Principal")
    @pytest.mark.smoke
    def test_novo_cenario(self):
        with allure.step("Passo 1"):
            # Implementação
            pass
```

#### 2. Boas Práticas:
- ✅ Use **Page Object Model**
- ✅ Adicione **marcadores pytest**
- ✅ Inclua **Allure steps**
- ✅ Capture **screenshots**
- ✅ Aguarde **elementos aparecerem**
- ✅ Valide **resultados esperados**

### 🎭 Expandindo Page Objects

#### Novo Elemento:
```python
# home_page.py
NOVO_BOTAO = (By.ID, "novoBotao")

def clicar_novo_botao(self) -> bool:
    """Clicar no novo botão."""
    try:
        sucesso = self.clicar(self.NOVO_BOTAO)
        if sucesso:
            logger.info("Novo botão clicado")
        return sucesso
    except Exception as e:
        logger.error(f"Erro ao clicar novo botão: {e}")
        return False
```

### 📊 Novos Dados de Teste

#### Arquivo JSON:
```json
{
  "novo_cenario": {
    "campo1": "valor1",
    "campo2": "valor2",
    "descricao": "Descrição do cenário",
    "resultado_esperado": "esperado"
  }
}
```

#### Fixture:
```python
@pytest.fixture
def dados_novo_cenario():
    """Dados para novo cenário."""
    return {
        'campo1': 'valor1',
        'campo2': 'valor2'
    }
```

### 🔧 Configurações Personalizadas

#### Novo Marcador:
```ini
# pytest.ini
markers =
    novo_tipo: Descrição do novo tipo de teste
```

#### Nova Configuração:
```properties
# ambiente.properties
nova.configuracao=valor
timeout.novo.processo=60
```

### 📈 Métricas e Monitoramento

#### Performance:
```python
def test_performance_nova_funcionalidade(self, performance_monitor):
    performance_monitor.iniciar("nova_operacao")
    
    # Operação a ser medida
    resultado = self.executar_operacao()
    
    tempo = performance_monitor.finalizar("nova_operacao")
    assert tempo < 10, f"Operação muito lenta: {tempo:.2f}s"
```

---

## 🎯 Critérios de Qualidade

### ✅ Performance
- **Análise ML**: < 10 segundos
- **Fluxo Completo**: < 30 segundos
- **Carregamento**: < 5 segundos
- **Preenchimento**: < 2 segundos

### ✅ Estabilidade
- **Taxa de Sucesso**: > 95%
- **Falhas Intermitentes**: < 5%
- **Recuperação**: Automática
- **Evidências**: Completas

### ✅ Cobertura
- **Fluxos Principais**: 100%
- **Validações**: 90%
- **Responsividade**: 100%
- **Cenários de Erro**: 80%

### ✅ Manutenibilidade
- **Page Objects**: Estruturados
- **Documentação**: Completa
- **Configurações**: Externalizadas
- **Logs**: Detalhados

---

## 🚀 Integração CI/CD

### 🔄 Pipeline Sugerido

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
          
      - name: Install dependencies
        run: |
          cd back-end/Testes/E2E
          pip install -r requirements.txt
          
      - name: Start FetalCare services
        run: |
          # Comandos para iniciar sistema
          
      - name: Run E2E tests
        run: |
          cd back-end/Testes/E2E
          pytest -m smoke --headless --alluredir=allure-results
          
      - name: Generate Allure report
        run: |
          allure generate allure-results -o allure-report
          
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: allure-report
          path: allure-report/
```

### 📊 Métricas de CI/CD
- **Execução**: Automática em PR/push
- **Tempo**: < 15 minutos
- **Relatórios**: Anexados automaticamente
- **Notificação**: Em falhas

---

## 🎉 Conclusão

### ✅ Implementação Completa
Os testes E2E do FetalCare fornecem uma **cobertura completa** dos fluxos principais do sistema, garantindo que:

- 🎯 **Funcionalidade**: Todos os recursos funcionam corretamente
- 🔒 **Qualidade**: Padrão profissional de implementação
- 📊 **Confiabilidade**: Validação automática contínua
- 🚀 **Manutenibilidade**: Estrutura escalável e documentada

### 🏆 Benefícios
- **Detecção Precoce**: Problemas encontrados rapidamente
- **Regressão**: Proteção contra quebras
- **Documentação Viva**: Testes como especificação
- **Confiança**: Deploy seguro em produção

### 📈 Evolução Contínua
A estrutura implementada permite **expansão fácil** para:
- Novos cenários de teste
- Diferentes navegadores
- Ambientes de teste
- Integração com outras ferramentas

---

**🎯 Os testes E2E do FetalCare representam uma implementação de classe mundial para garantir a qualidade do sistema de monitoramento fetal, seguindo as melhores práticas da indústria e fornecendo uma base sólida para o desenvolvimento contínuo.**

---

*📅 Última atualização: 19 de dezembro de 2024*  
*🏥 Sistema: FetalCare - Monitoramento Fetal*  
*🧪 Versão: 2.0.0 - Testes E2E Completos*  
*👨‍💻 Implementação: Equipe de QA* 