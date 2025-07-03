# Dockerfile para Apresentação FetalCare
FROM python:3.11-slim

# Metadados
LABEL maintainer="Universidade Católica de Brasília"
LABEL description="Sistema FetalCare - Apresentação Interativa"
LABEL version="1.0"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY app_fetalcare.py .
COPY README_APRESENTACAO.md .

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash streamlit
USER streamlit

# Expor porta
EXPOSE 8501

# Configurar Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_HEADLESS=true

# Comando de inicialização
CMD ["streamlit", "run", "app_fetalcare.py", "--server.port=8501", "--server.address=0.0.0.0"] 