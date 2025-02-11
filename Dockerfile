# Usa uma imagem base Python otimizada
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Define o ponto de entrada para o Lambda
CMD ["python", "-m", "lambda_handler"]
