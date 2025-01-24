# Use a imagem base do Python
FROM python:3.10-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o conteúdo do diretório atual para o diretório de trabalho no container
COPY . /app

# Instale as dependências
RUN pip install -r requirements.txt

# Comando para iniciar o servidor ASGI, ajustando o caminho para 'app.main:app'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
