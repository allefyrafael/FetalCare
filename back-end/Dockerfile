# Use uma imagem Python oficial como base
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta 5000
EXPOSE 5000

# Configurar variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando para executar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"] 