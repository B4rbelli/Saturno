# Dockerfile
FROM python:3.12-slim

# Diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt

# Expõe a porta usada pelo FastAPI/Uvicorn
EXPOSE 8000

# Comando que roda a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
