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
  python3 manage.py compilemessages
}

run_server() {
  if bool "$DEV_SERVER"; then
    printc "Starting Django development server...\n" "info"
    python3 manage.py runserver 0.0.0.0:8000
  else
    printc "Starting Gunicorn server...\n" "info"
    gunicorn {{ project_name }}.wsgi --bind 0.0.0.0:8000
  fi
}

fail_isort() {
  printc "Issues found by 'isort'! " "danger"
  printc "Check the output above to locate and fix the issues\n" "danger"
  exit 1
}

START_ARG="start"
TEST_ARG="test"
CHECK_ARG="check"
FIX_ARG="fix"
TEST_COVERAGE_PERCENTAGE=${TEST_COVERAGE_PERCENTAGE:-100}

#########################################################################
# START: execution ######################################################
#########################################################################
if [ "$1" = "$START_ARG" ]; then
  wait_for_postgres
  init_django_project
  run_server

elif [ "$1" = "$TEST_ARG" ]; then
  printc "Running tests (pytest) with expected $TEST_COVERAGE_PERCENTAGE% coverage...\n" "info"
  pytest --cov --cov-report term:skip-covered --cov-fail-under="$TEST_COVERAGE_PERCENTAGE" -n auto

elif [ "$1" = "$CHECK_ARG" ]; then
  printc "[flake8] Checking linting issues...\n" "info"
  flake8 --toml-config=pyproject.toml .

  printc "[isort] Checking issues with imports...\n" "info"
  isort --check . && printc "No issues with imports.\n" "success" || fail_isort

elif [ "$1" = "$FIX_ARG" ]; then
  printc "[isort] Fixing issues with imports...\n" "info"
  isort .

else
  printc "Unknown argument: \"$1\" \n" "danger"
  printc "Available first arguments: \"$START_ARG\" \n" "info"
  printc "Exiting!\n" "info"
  exit 1
fi
#########################################################################
# END: execution ########################################################
#########################################################################
