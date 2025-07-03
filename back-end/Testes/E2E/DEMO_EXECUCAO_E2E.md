# 🚀 Demo de Execução - Testes E2E FetalCare

## 📋 Guia Prático de Demonstração

Este guia fornece instruções passo-a-passo para demonstrar os testes E2E do sistema FetalCare em funcionamento.

---

## 🎯 Pré-requisitos

### ✅ Checklist Antes da Demonstração

```bash
# 1. Verificar Python
python --version
# Esperado: Python 3.8+

# 2. Verificar pip
pip --version

# 3. Navegar para pasta E2E
cd back-end/Testes/E2E

# 4. Verificar arquivos essenciais
ls -la
# Deve listar: requirements.txt, conftest.py, pytest.ini, etc.
```

### 🌐 Serviços do FetalCare
Certifique-se de que o sistema está rodando:

```bash
# Frontend (obrigatório)
curl http://localhost:8080
# Esperado: HTML da página principal

# API (obrigatório)  
curl http://localhost:5001/health
# Esperado: {"status": "healthy"}

# MongoDB (verificação opcional)
# Porta 27017 deve estar aberta
```

---

## 📦 Instalação Rápida

### 🚀 Setup em 3 Minutos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar ChromeDriver (automático)
python scripts/setup_chromedriver.py

# 3. Verificar instalação
pytest --version
```

### ⚠️ Solução de Problemas Comuns

```bash
# Se ChromeDriver falhar
pip install webdriver-manager

# Se Selenium falhar
pip install selenium==4.15.2

# Se pytest falhar
pip install pytest==7.4.3
```

---

## 🎮 Demonstração Interativa

### 🚀 Execução Principal

```bash
# Executar menu interativo
python scripts/run_e2e_tests.py
```

**Tela inicial esperada:**
```
======================================================================
🧪 EXECUTOR DE TESTES E2E - SISTEMA FETALCARE 🧪
======================================================================
Sistema de monitoramento fetal com análise por Machine Learning
Testes automatizados End-to-End com Selenium WebDriver
======================================================================

🔍 Verificando pré-requisitos...

📋 Status dos Pré-requisitos:
  ✅ Python               - Versão: 3.9.0
  ✅ pytest               - pytest 7.4.3
  ✅ Selenium              - Versão: 4.15.2
  ✅ ChromeDriver          - Disponível em: /path/to/chromedriver
  ✅ Frontend (8080)       - Respondendo
  ✅ API (5001)           - Respondendo

✅ Pré-requisitos essenciais atendidos!
```

### 📋 Menu de Opções

```
📋 MENU PRINCIPAL
──────────────────────────────────────────────────
  1 - 🎯 Executar Fluxo Completo
      Teste do fluxo principal end-to-end
  2 - 📝 Executar Testes de Formulário
      Validações de campos e preenchimento
  3 - 🤖 Executar Testes de Análise ML
      Testes específicos da análise de ML
  4 - 🔍 Executar Testes de Validação
      Testes de validação e tratamento de erros
  5 - 📱 Executar Testes de Responsividade
      Testes em diferentes resoluções
  6 - 🚀 Executar TODOS os Testes
      Suite completa de testes E2E
  7 - 📊 Gerar Relatório
      Gerar relatório dos últimos testes
  8 - 🔧 Configurações
      Ajustar configurações de execução
  9 - ❓ Ajuda
      Informações sobre uso dos testes
  0 - 🚪 Sair
      Encerrar programa
──────────────────────────────────────────────────

👉 Escolha uma opção (0-9):
```

---

## 🎭 Demonstração do Fluxo Completo

### 📝 Cenário Principal (Opção 1)

1. **Selecionar opção 1** no menu
2. **Configurar execução**:

```
⚙️  CONFIGURAÇÕES DE EXECUÇÃO
────────────────────────────────────────
🖥️  Executar em modo headless (sem interface gráfica)? [s/N]: N
📸 Capturar screenshots sempre (não só em falhas)? [s/N]: s
⚡ Executar testes em paralelo? [S/n]: n
⏱️  Timeout para testes em segundos [300]: 300
```

3. **Execução iniciada**:

```
🚀 Executando Testes de Fluxo Completo
Testando o fluxo principal end-to-end do sistema
────────────────────────────────────────────────────────────
📝 Comando: pytest cenarios/test_fluxo_completo.py -v -m critical or smoke --capture-screenshots
⏰ Iniciando em 3 segundos...
```

### 🎬 Sequência de Execução Visível

**Você verá o navegador:**

1. **🌐 Abrir Chrome** (janela maximizada)
2. **📄 Carregar página** `http://localhost:8080`
3. **✅ Verificar status** (conexão online)
4. **📝 Preencher gestante**:
   - Nome: "Maria Silva Santos"
   - ID: "P001"
   - CPF: "123.456.789-00"
   - Idade Gestacional: 28
   - Idade: 30
5. **💾 Salvar dados da gestante**
6. **📊 Preencher monitoramento**:
   - Baseline: 140 bpm
   - Acelerações: 3
   - Movimento fetal: 5
   - (21 parâmetros no total)
7. **🤖 Executar análise ML**
8. **⏳ Aguardar loading** (8-10 segundos)
9. **📋 Exibir resultados**:
   - Status: NORMAL
   - Recomendações
   - Detalhes
10. **💾 Salvar resultados**
11. **🔗 Navegar para registros**
12. **✅ Verificar salvamento**

### 📊 Output do Terminal

```
test_fluxo_completo.py::TestFluxoCompleto::test_fluxo_completo_normal PASSED [100%]

==================== PASSOS EXECUTADOS ====================
✅ 1. Verificar estado inicial da página
✅ 2. Preencher dados da gestante  
✅ 3. Salvar dados da gestante
✅ 4. Preencher parâmetros de monitoramento
✅ 5. Executar análise fetal
✅ 6. Verificar resultados da análise
✅ 7. Salvar resultados
✅ 8. Navegar para página de registros  
✅ 9. Verificar que registro foi salvo

==================== MÉTRICAS ====================
⏱️  Tempo total: 21.5s
📸 Screenshots: 9 capturas
🤖 Análise ML: 8.7s
📊 Resultado: NORMAL
==================== 1 passed in 21.50s ====================

✅ Execução concluída com sucesso!
⏱️  Tempo total: 21.5 segundos
```

---

## 🔬 Demonstração de Casos Específicos

### 🚨 Teste com Parâmetros de Risco

**Execução manual:**
```bash
pytest cenarios/test_fluxo_completo.py::TestFluxoCompleto::test_fluxo_completo_risco -v -s
```

**Parâmetros usados:**
- Baseline: 180 bpm (taquicardia)
- Acelerações: 0 (ausentes)
- Movimento fetal: 1 (reduzido)
- Decelerações severas: 3

**Resultado esperado:**
- ⚠️ Status: RISCO ou CRÍTICO
- 📋 Recomendações específicas
- 🚨 Alertas médicos

### ⚡ Teste de Performance

```bash
pytest cenarios/test_fluxo_completo.py::TestFluxoCompleto::test_performance_fluxo_completo -v
```

**Critérios validados:**
- ✅ Análise ML < 10 segundos
- ✅ Fluxo completo < 30 segundos
- ✅ Carregamento página < 5 segundos

---

## 📱 Demonstração de Responsividade

### 🖥️ Múltiplas Resoluções

```bash
# Executar teste de responsividade
python scripts/run_e2e_tests.py
# Escolher opção 5
```

**Sequência de execução:**
1. **Desktop** (1920x1080) - Layout completo
2. **Tablet** (768x1024) - Layout adaptado  
3. **Mobile** (375x667) - Layout responsivo

**Validações:**
- ✅ Formulários acessíveis
- ✅ Botões clicáveis
- ✅ Navegação funcional
- ✅ Texto legível

---

## 📊 Geração de Relatórios

### 📈 Relatório Allure (Recomendado)

```bash
# Opção 7 no menu principal
python scripts/run_e2e_tests.py
# Escolher: 7 - 📊 Gerar Relatório
```

**Processo automático:**
1. 🔍 Verificar resultados existentes
2. 📊 Gerar relatório Allure
3. 🌐 Abrir no navegador

**Conteúdo do relatório:**
- 📊 Dashboard com estatísticas
- 📈 Gráficos de execução
- 🖼️ Screenshots em falhas
- 📝 Logs detalhados
- ⏱️ Métricas de performance
- 📋 Histórico de execuções

### 📄 Relatório HTML Simples

```bash
# Execução direta
pytest --html=relatorios/html/report.html --self-contained-html
```

---

## 🔍 Demonstração de Debugging

### 🐛 Modo Debug Interativo

```bash
# Executar com pausa em falhas
pytest cenarios/test_fluxo_completo.py --pdb -v

# Executar com logs verbosos
pytest cenarios/test_fluxo_completo.py -v -s --log-cli-level=INFO
```

### 📸 Screenshots Manuais

Durante a execução, adicione no código:
```python
# Capturar screenshot específico
self.home_page.obter_screenshot("momento_específico")
```

### 🔍 Inspeção Manual

```python
# Adicionar pausa para inspeção
import time
time.sleep(10)  # Pausa de 10 segundos
```

---

## 🚀 Execução Rápida (Linha de Comando)

### ⚡ Comandos Essenciais

```bash
# Fluxo completo (mais comum)
pytest cenarios/test_fluxo_completo.py -v

# Todos os testes críticos
pytest -m critical -v

# Testes rápidos (smoke)
pytest -m smoke --headless

# Execução paralela
pytest -n auto

# Com timeout personalizado
pytest --timeout=60

# Headless (sem abrir navegador)
pytest --headless

# Com screenshots sempre
pytest --capture-screenshots
```

### 📊 Execução com Relatórios

```bash
# HTML + Allure completo
pytest --html=relatorios/html/report.html --alluredir=relatorios/allure-results

# Gerar e abrir Allure
allure generate relatorios/allure-results -o relatorios/allure-report
allure open relatorios/allure-report
```

---

## 🎯 Demonstração para Diferentes Públicos

### 👨‍💼 Para Gestores (5 minutos)

1. **Mostrar menu interativo**
2. **Executar fluxo completo** (opção 1)
3. **Destacar:**
   - ✅ Automatização completa
   - ⏱️ Tempo de execução (20s)
   - 📊 Validação da análise ML
   - 📈 Relatórios profissionais

### 👨‍💻 Para Desenvolvedores (15 minutos)

1. **Mostrar estrutura de código**
2. **Page Object Model**
3. **Execução com logs verbosos**
4. **Screenshots de debugging**
5. **Configurações personalizáveis**

### 🧪 Para QA (30 minutos)

1. **Todos os tipos de teste**
2. **Dados de teste variados**
3. **Cenários de falha**
4. **Relatórios detalhados**
5. **Configuração de CI/CD**

---

## 📋 Checklist de Demonstração

### ✅ Antes da Demo
- [ ] Sistema FetalCare rodando
- [ ] Dependências instaladas
- [ ] ChromeDriver configurado
- [ ] Dados de teste preparados
- [ ] Navegador fechado (para visualização)

### ✅ Durante a Demo
- [ ] Explicar objetivo dos testes E2E
- [ ] Mostrar menu interativo
- [ ] Executar fluxo principal
- [ ] Destacar automação completa
- [ ] Mostrar relatórios gerados
- [ ] Demonstrar flexibilidade

### ✅ Após a Demo
- [ ] Disponibilizar documentação
- [ ] Explicar processo de manutenção
- [ ] Discutir integração CI/CD
- [ ] Cronograma de execução

---

## 🔧 Personalização da Demo

### 🎨 Configurações Visuais

```bash
# Execução mais lenta (para visualização)
pytest --slow-motion

# Destaque de elementos
pytest --highlight-elements

# Janela menor
pytest --window-size=1280,720
```

### 📊 Dados Customizados

Edite `dados/gestantes_validas.json`:
```json
{
  "nome": "Demo Gestante",
  "id": "DEMO001",
  "idade_gestacional": 32
}
```

### ⏱️ Timeouts Ajustados

Edite `configuracao/ambiente.properties`:
```properties
timeout.analysis=30
screenshot.always=true
slow.motion=true
```

---

## 🎯 Resultados Esperados da Demo

### ✅ Métricas de Sucesso
- 🎯 **Execução**: 100% dos testes passam
- ⏱️ **Performance**: Critérios atendidos
- 📸 **Evidências**: Screenshots gerados
- 📊 **Relatórios**: HTML + Allure funcionais

### 📊 Tempo Total da Demo
- **Demonstração rápida**: 5-10 minutos
- **Demonstração completa**: 15-30 minutos
- **Workshop técnico**: 45-60 minutos

### 🎉 Resultado Final
Ao final da demonstração, você terá mostrado uma **implementação completa e profissional** de testes E2E que:

- ✅ Valida todo o fluxo do sistema
- ✅ Funciona de forma automática
- ✅ Gera relatórios profissionais
- ✅ É fácil de executar e manter
- ✅ Segue as melhores práticas da indústria

---

**🎯 A demonstração comprova que o sistema FetalCare possui uma cobertura de testes E2E robusta e profissional, garantindo a qualidade do sistema de monitoramento fetal.**

---

*📅 Última atualização: 19 de dezembro de 2024*  
*🏥 Sistema: FetalCare - Monitoramento Fetal*  
*🧪 Implementação: Testes E2E Completos* 