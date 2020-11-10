#!/bin/sh

echo "Waiting for postgres..."

while ! pg_isready -h db; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py collectstatic --clear --no-input
python manage.py migrate

if [ $(psql -qtA "postgresql://$SQL_USER:$SQL_PASSWORD@$SQL_HOST/$SQL_DATABASE" -c "select exists (select * from main_sale limit 1)") != "t" ]; then
  python manage.py importdata  # import data if doesn't exist
fi

gunicorn housing_prices.wsgi:application --bind 0.0.0.0:8000
