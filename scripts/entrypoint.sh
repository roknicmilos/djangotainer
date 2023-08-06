#!/bin/bash

set -e

. /app/scripts/utils.sh

wait_for_postgres() {
  # Adapted from https://docs.docker.com/compose/startup-order/
  printc "Waiting for PostgreSQL...\n" "info"
  until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOSTNAME" -U "$DB_USERNAME" -d "$DB_NAME" -c '\q'; do
    printc >&2 "Postgres is unavailable - sleeping\n" "info"
    sleep 1
  done
}

init_django_project() {
  if bool "$COLLECT_STATIC_FILES"; then
    python3 manage.py collectstatic --noinput
  fi
  python3 manage.py migrate
  python3 manage.py createsuperuser --noinput || true
}

run_server() {
  if bool "$DEV_SERVER"; then
    printc "Starting Django development server...\n" "info"
    python3 manage.py runserver 0.0.0.0:8000
  else
    printc "Starting Gunicorn server...\n" "info"
    gunicorn meme_wars.wsgi --bind 0.0.0.0:8000
  fi
}

START_ARG="start"

#########################################################################
# START: execution ######################################################
#########################################################################
if [ "$1" = "$START_ARG" ]; then
  wait_for_postgres
  init_django_project
  run_server
else
  printc "Unknown argument: \"$1\" \n" "danger"
  printc "Available first arguments: \"$START_ARG\" \n" "info"
  printc "Exiting!\n" "info"
  exit 1
fi
#########################################################################
# END: execution ########################################################
#########################################################################