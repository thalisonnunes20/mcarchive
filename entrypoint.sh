#!/bin/sh
set -e

if [ -n "$DB_NAME" ] && [ "$DB_ENGINE" != "django.db.backends.sqlite3" ]; then
  echo "==> Banco PostgreSQL detectado ($DB_NAME). Aguardando conexao..."
  until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-mcarchive_user}"; do
    >&2 echo "PostgreSQL ainda nao esta pronto - aguardando..."
    sleep 2
  done
  echo "==> PostgreSQL conectado com sucesso!"
else
  echo "==> Nenhuma variavel de PostgreSQL definida (ou SQLite configurado). Usando SQLite local!"
fi

echo "==> Aplicando migracoes..."
python manage.py migrate --noinput

echo "==> Coletando arquivos estaticos..."
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "==> Criando superuser automatico ($DJANGO_SUPERUSER_USERNAME)..."
  python manage.py createsuperuser --noinput || true
fi

echo "==> Iniciando Nginx e Gunicorn via Supervisor..."
exec "$@"
