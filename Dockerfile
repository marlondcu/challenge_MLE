# syntax=docker/dockerfile:1.2
FROM python:3.10


# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app
 
# Copie os arquivos necessários
COPY . /app

# Instale as dependências
#RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8080 para o Cloud Run
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
