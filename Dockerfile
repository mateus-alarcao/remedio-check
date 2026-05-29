FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/       ./src/
COPY tests/     ./tests/
COPY pyproject.toml .

# Copia o .env se existir (para rodar localmente via Docker)
# Em produção, passe as variáveis via -e ou --env-file
COPY .env* ./

CMD ["python", "src/app.py"]
