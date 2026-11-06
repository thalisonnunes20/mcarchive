#!/bin/sh
set -e

if [ -n "$DB_NAME" ] && [ "$DB_ENGINE" != "django.db.backends.sqlite3" ]; then
  echo "==> Banco PostgreSQL detectado ($DB_NAME). Aguardando conexão..."
  until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-mcarchive_user}"; do
    >&2 echo "PostgreSQL ainda não está pronto - aguardando..."
    sleep 2
  done
  echo "==> PostgreSQL conectado com sucesso!"
else
  echo "==> Nenhuma variável de PostgreSQL definida (ou SQLite configurado). Usando SQLite local!"
fi

echo "==> Aplicando migrações..."
python manage.py migrate --noinput

echo "==> Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Iniciando aplicação..."
exec "$@"
