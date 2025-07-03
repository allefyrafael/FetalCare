# FetalCare API - Sistema de Banco de Dados

## 🎯 **Resumo do Sistema**

Sistema completo para gerenciamento de registros de exames fetais com:
- **MongoDB** como banco de dados não relacional
- **FastAPI** para API REST
- **Integração** com modelo ML existente
- **Classificação automática** do status de saúde fetal

## 🏗️ **Estrutura do Projeto**

```
back-end/
├── banco/                    # Módulo do banco de dados
│   ├── models.py            # Modelos Pydantic/MongoDB
│   ├── database.py          # Conexão MongoDB
│   ├── crud.py              # Operações CRUD
│   └── ml_client.py         # Cliente API ML
├── fastapi/                 # API FastAPI
│   ├── main.py              # App principal
│   ├── config.py            # Configurações
│   └── requirements.txt     # Dependências
└── test_api_fetalcare.py    # Testes
```

## 📊 **Modelo de Dados**

### Registro de Exame Completo:
- **Dados da Gestante**: ID, nome, CPF, idade gestacional, etc.
- **Parâmetros ML**: 21 campos do modelo de machine learning
- **Resultado ML**: Predição, confidence, status, recomendações
- **Saúde do Feto**: Status calculado baseado na confidence
- **Metadados**: Data, médico responsável, observações

### Lógica de Status:
| Confidence | Status | Risco |
|-----------|--------|-------|
| ≤ 55% | Risco Crítico | CRÍTICO |
| 56-65% | Em Risco | MODERADO |
| ≥ 66% | Normal | BAIXO |

## 🚀 **APIs Disponíveis**

### Principais Endpoints:
- `POST /registros` - Cria registro, chama ML, salva resultado
- `GET /registros` - Lista todos os registros
- `GET /registros?cpf=...` - Filtra por CPF
- `GET /registros/{id}` - Obtém registro específico
- `GET /estatisticas` - Estatísticas dos registros

## ⚡ **Instalação Rápida**

### 1. MongoDB (Docker)
```bash
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

### 2. Instalar Dependências
```bash
cd back-end/fastapi
pip install -r requirements.txt
```

### 3. Executar API
```bash
python main.py
```

### 4. Testar
```bash
cd back-end
python test_api_fetalcare.py
```

## 🔗 **URLs Importantes**
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs
- Health Check: http://localhost:8000/

## 🧪 **Exemplo de Uso**

```python
import httpx

# Dados de exemplo
dados = {
    "dados_gestante": {
        "patient_id": "G2024001",
        "patient_name": "Maria Silva",
        "patient_cpf": "123.456.789-00",
        "gestational_age": 28
    },
    "parametros_monitoramento": {
        "baseline_value": 140.0,
        "accelerations": 3,
        "fetal_movement": 4,
        # ... outros 18 parâmetros
    }
}

# Criar registro
response = httpx.post("http://localhost:8000/registros", json=dados)
print(response.json())
```

## ✅ **Status do Sistema**
- ✅ Modelos de dados definidos
- ✅ Conexão MongoDB configurada  
- ✅ CRUD completo implementado
- ✅ Integração com API ML
- ✅ Classificação de saúde automática
- ✅ API FastAPI funcional
- ✅ Testes automatizados
- ✅ Documentação completa

**Pronto para uso!** 🎉 