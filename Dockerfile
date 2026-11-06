FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Instala ferramentas essenciais, PostgreSQL client, Nginx e Supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    postgresql-client \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Remove o site default do Nginx para evitar conflito na porta 80
RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default

# Copia requisitos e instala dependencias de producao
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/production.txt

# Copia todo o codigo da aplicacao
COPY . /app/

# Configura Nginx e Supervisor dentro do container
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Cria pastas necessarias e garante permissao no entrypoint
RUN mkdir -p /app/staticfiles /app/media /app/logs /app/data && \
    chmod +x /app/entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
