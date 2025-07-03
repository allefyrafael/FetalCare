# 📋 MATRIZ DE RASTREABILIDADE
## Requisitos vs Casos de Teste - Sistema FetalCare

### 📅 **Informações do Documento**
- **Data**: 03 de Julho de 2025
- **Versão**: 1.0

---

## 🎯 **OBJETIVO**

Esta matriz estabelece a rastreabilidade entre:
- **Requisitos Funcionais** do sistema FetalCare
- **Casos de Teste** que validam cada requisito
- **Tipos de Teste** aplicáveis
- **Prioridade** e **Risco** associados

---

## 📊 **LEGENDA**

### **Tipos de Teste**
- **UT**: Testes Unitários
- **IT**: Testes de Integração
- **PT**: Testes de Performance
- **E2E**: Testes End-to-End


### **Prioridade**
- **P1**: Crítica (Bloqueante)
- **P2**: Alta (Importante)
- **P3**: Média (Desejável)
- **P4**: Baixa (Opcional)

### **Risco**
- **🔴**: Alto Risco
- **🟡**: Médio Risco
- **🟢**: Baixo Risco

---

## 🏗️ **REQUISITOS FUNCIONAIS**

### **RF01 - Sistema de Predição ML**
| ID | Requisito | Casos de Teste | Tipos | Prioridade | Risco | Status |
|----|-----------|----------------|-------|------------|-------|--------|
| RF01.1 | Carregar modelo ML | TC001, TC002 | UT, IT | P1 | 🔴 | ✅ |
| RF01.2 | Processar 21 parâmetros | TC003, TC004, TC005 | UT, IT | P1 | 🔴 | ✅ |
| RF01.3 | Calcular confidence | TC006, TC007 | UT | P1 | 🔴 | ✅ |
| RF01.4 | Classificar status (1,2,3) | TC008, TC009, TC010 | UT, IT | P1 | 🔴 | ✅ |
| RF01.5 | Gerar recomendações | TC011, TC012 | UT | P2 | 🟡 | ✅ |

### **RF02 - Interface Web**
| ID | Requisito | Casos de Teste | Tipos | Prioridade | Risco | Status |
|----|-----------|----------------|-------|------------|-------|--------|
| RF02.1 | Formulário dados gestante | TC013, TC014 | E2E | P1 | 🟡 | ✅ |
| RF02.2 | Entrada parâmetros monitoramento | TC015, TC016 | E2E | P1 | 🟡 | ✅ |
| RF02.3 | Exibir resultados predição | TC017, TC018 | E2E | P1 | 🟡 | ✅ |
| RF02.4 | Navegação entre páginas | TC019, TC020 | E2E | P2 | 🟢 | ✅ |
| RF02.5 | Responsividade | TC021, TC022 | E2E | P2 | 🟢 | ⏳ |

### **RF03 - Banco de Dados**
| ID | Requisito | Casos de Teste | Tipos | Prioridade | Risco | Status |
|----|-----------|----------------|-------|------------|-------|--------|
| RF03.1 | Salvar predições | TC023, TC024 | IT | P1 | 🔴 | ✅ |
| RF03.2 | Consultar registros | TC025, TC026 | IT | P1 | 🟡 | ✅ |
| RF03.3 | Filtrar por CPF | TC027, TC028 | IT | P2 | 🟡 | ✅ |
| RF03.4 | Filtrar por status | TC029, TC030 | IT | P2 | 🟡 | ✅ |
| RF03.5 | Gerar estatísticas | TC031, TC032 | IT | P2 | 🟢 | ✅ |

### **RF04 - API REST**
| ID | Requisito | Casos de Teste | Tipos | Prioridade | Risco | Status |
|----|-----------|----------------|-------|------------|-------|--------|
| RF04.1 | Endpoint health check | TC033, TC034 | UT, IT | P1 | 🟢 | ✅ |
| RF04.2 | Endpoint predição | TC035, TC036, TC037 | UT, IT | P1 | 🔴 | ✅ |
| RF04.3 | Endpoint listagem | TC038, TC039 | UT, IT | P1 | 🟡 | ✅ |
| RF04.4 | Endpoint estatísticas | TC040, TC041 | UT, IT | P2 | 🟡 | ✅ |
| RF04.5 | Validação de entrada | TC042, TC043, TC044 | UT | P1 | 🔴 | ⚠️ |


---

## 📈 **REQUISITOS NÃO FUNCIONAIS**

### **RNF01 - Performance**
| ID | Requisito | Casos de Teste | Tipos | Prioridade | Risco | Status |
|----|-----------|----------------|-------|------------|-------|--------|
| RNF01.1 | Tempo resposta < 300ms | TC055, TC056 | PT | P1 | 🔴 | ⏳ |
| RNF01.2 | Suporte 100 usuários | TC057, TC058 | PT | P1 | 🔴 | ⏳ |
| RNF01.3 | Throughput > 50 req/s | TC059, TC060 | PT | P2 | 🟡 | ⏳ |
| RNF01.4 | Sem vazamentos memória | TC061, TC062 | PT | P2 | 🟡 | ⏳ |

### **RNF02 - Confiabilidade**
| ID | Requisito | Casos de Teste | Tipos | Prioridade | Risco | Status |
|----|-----------|----------------|-------|------------|-------|--------|
| RNF02.1 | Disponibilidade 99.9% | TC063, TC064 | PT | P1 | 🔴 | ⏳ |
| RNF02.2 | Recuperação falhas | TC065, TC066 | IT | P1 | 🔴 | ❌ |
| RNF02.3 | Backup dados | TC067, TC068 | IT | P1 | 🔴 | ❌ |
| RNF02.4 | Monitoramento | TC069, TC070 | IT | P2 | 🟡 | ❌ |

### **RNF03 - Usabilidade**
| ID | Requisito | Casos de Teste | Tipos | Prioridade | Risco | Status |
|----|-----------|----------------|-------|------------|-------|--------|
| RNF03.1 | Interface intuitiva | TC071, TC072 | E2E | P2 | 🟡 | ⏳ |
| RNF03.2 | Cross-browser | TC073, TC074, TC075 | E2E | P2 | 🟡 | ⏳ |
| RNF03.3 | Acessibilidade | TC076, TC077 | E2E | P3 | 🟢 | ❌ |
