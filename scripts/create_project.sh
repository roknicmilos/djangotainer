#!/bin/bash

# Requirements:
#   - Python 3
#   - Docker and Docker Compose
#   - venv (Python module)

# Steps:
#   1. Go to parent directory of "djangotainer" project
#   2. Make this script executable: `chmod +x djangotainer/scripts/create_project.sh`
#   3. Run the script: `djangotainer/scripts/create_project.sh [start] [--build]`

set -e

. djangotainer/scripts/utils.sh

START_ARG="start"
BUILD_ARG="--build"

create_project() {
  printc "Creating directory \"djangotainer_example\" \n" "info"
  mkdir djangotainer_example

  printc "Creating Python virtual environment (venv) \n" "info"
  python3 -m venv djangotainer_example/venv

  printc "Activating Python virtual environment (venv) \n" "info"
  source djangotainer_example/venv/bin/activate

  printc "Installing Django \n" "info"
  pip install django

  printc "Creating new Django project from \"djangotainer\" template \n" "info"
  django-admin startproject --template djangotainer \
    --name=pyproject.toml,docker-compose.yml,example.env \
    djangotainer_example ./djangotainer_example

  printc "Deactivating Python virtual environment (venv) \n" "info"
  deactivate

  printc "Removing Python virtual environment directory (venv) \n" "info"
  rm -rf djangotainer_example/venv
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
  printc "Preparing environment variables \n" "info"
  cd djangotainer_example
  cp example.env .env

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
