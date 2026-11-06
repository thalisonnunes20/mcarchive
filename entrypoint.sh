#!/bin/sh
set -e

echo "==> Aguardando inicialização do banco de dados PostgreSQL..."
until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-mcarchive_user}"; do
  >&2 echo "PostgreSQL ainda não está pronto - aguardando..."
  sleep 2
done

echo "==> PostgreSQL conectado com sucesso!"

echo "==> Aplicando migrações..."
python manage.py migrate --noinput

echo "==> Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Iniciando aplicação..."
exec "$@"

