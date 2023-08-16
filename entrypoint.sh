#!/bin/sh

echo 'Waiting for postgres...'

while ! nc -z $DB_HOSTNAME $DB_PORT; do
    sleep 0.1
done

echo 'PostgreSQL started'

# Create and configure the database user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER spoopy WITH PASSWORD '$DB_PASSWORD';
  ALTER ROLE spoopy SET client_encoding TO 'utf8';
  ALTER ROLE spoopy SET default_transaction_isolation TO 'read committed';
  ALTER ROLE spoopy SET timezone TO 'UTC';
  GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO spoopy;
EOSQL

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

exec "$@"
