#!/bin/bash

# Requirements:
#   - Python 3
#   - Docker and Docker Compose
#   - venv (Python module)

# Steps:
#   1. Make this script executable: `chmod +x djangotainer/scripts/create_project.sh`
#   2. Run the script: `djangotainer/scripts/create_project.sh [start] [--build]`

set -e

. djangotainer/scripts/utils.sh

START_ARG="start"
BUILD_ARG="--build"

create_project() {
  printc "Creating directory \"test_djangotainer\" \n" "info"
  mkdir test_djangotainer

  printc "Creating Python virtual environment (venv) \n" "info"
  python3 -m venv test_djangotainer/venv

  printc "Activating Python virtual environment (venv) \n" "info"
  source test_djangotainer/venv/bin/activate

  printc "Installing Django \n" "info"
  pip install django

  printc "Creating new Django project from \"djangotainer\" template \n" "info"
  django-admin startproject \
  --template=https://github.com/roknicmilos/djangotainer/archive/main.zip \
  --name=pyproject.toml,docker-compose.yml,example.env \
  test_djangotainer ./test_djangotainer

  printc "Deactivating Python virtual environment (venv) \n" "info"
  deactivate

  printc "Removing Python virtual environment directory (venv) \n" "info"
  rm -rf test_djangotainer/venv

  printc "Preparing environment variables \n" "info"
  cd test_djangotainer
  cp example.env .env
}

handle_second_arg() {
  if [ "$2" = "$BUILD_ARG" ]; then
    printc "Building images \n" "info"
    docker compose build
  else
    printc "Unknown second argument: \"$2\" \n" "danger"
    printc "Available second arguments: \"$BUILD_ARG\" \n" "info"
    printc "Exiting!\n" "info"
    exit 1
  fi
}

start_project() {
  if [ -n "$2" ]; then
    handle_second_arg "$@"
  fi

  printc "Starting containers \n" "info"
  docker compose up -d
}

validate_arguments() {
  if [ -n "$1" ]; then
    if [ "$1" != "$START_ARG" ]; then
      printc "Unknown first argument: \"$1\" \n" "danger"
      printc "Available first arguments: \"$START_ARG\" \n" "info"
      printc "Exiting!\n" "info"
      exit 1
    fi
  fi

  if [ -n "$2" ]; then
    if [ "$2" != "$BUILD_ARG" ]; then
      printc "Unknown second argument: \"$2\" \n" "danger"
      printc "Available second arguments: \"$BUILD_ARG\" \n" "info"
      printc "Exiting!\n" "info"
      exit 1
    fi
  fi
}

#########################################################################
# START: execution ######################################################
#########################################################################
validate_arguments "$@"
create_project
if [ "$1" = "$START_ARG" ]; then
  start_project "$@"
fi
#########################################################################
# END: execution ########################################################
#########################################################################
