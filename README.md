# djangotainer

This Django project template, built upon
[django-project-skeleton](https://django-project-skeleton.readthedocs.io/),
simplifies the creation of new Django projects.
It organizes all Django apps neatly within the `apps` directory.
Additionally, it includes essential, commonly used apps that aren't
part of Django's default package but are indispensable in nearly
every Django project.

---

Table of Contents
=================

* [Quickstart](#quickstart)
    * [Prerequisites](#prerequisites)
    * [Create a new Django project](#create-project)
    * [Start the project](#start-project)
* [Dependencies](#dependencies)
* [Preinstalled Django apps](docs/preinstalled-django-apps.md)
* [Development corner](docs/development-corner.md)

## Quickstart

### Prerequisites

- [Python](https://www.python.org/)
- [venv](https://docs.python.org/3/library/venv.html)
- [Docker](https://docs.docker.com/engine/install/) and
  [Docker Compose](https://docs.docker.com/compose/install/)

**NOTE**: Once you create a Django project using
[djangotainer](https://github.com/roknicmilos/djangotainer)
project template, the only prerequisite for that newly created
project will be [Docker](https://docs.docker.com/engine/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

### Create project

Below are the steps for creating a new Django project using the
[djangotainer](https://github.com/roknicmilos/djangotainer) project
template.

1. Create a new directory for the project:

   `mkdir [my_project]`

2. Create Python virtual environment [venv](https://docs.python.org/3/library/venv.html) in the project directory:

   `python3 -m venv [my_project]/venv`

3. Activate Python virtual environment:

   `source [my_project]/venv/bin/activate`

4. Install Django:

   `pip install django`

5. Create new Django project from "djangotainer" project template:

   ```shell
    django-admin startproject \
    --template=https://github.com/roknicmilos/djangotainer/archive/main.zip \
    --name=pyproject.toml,docker-compose.yml,example.env \
    test_djangotainer ./test_djangotainer
   ```

6. Deactivate and remove Python virtual environment:

   `deactivate && rm -rf [my_project]/venv`

### Start project

If you created a Django project by following the steps from the
[Create project](#create-project) section, you should now be able
to start that Django project by following the next steps:

1. Move to newly created Djagno project:

   `cd [my_project]`

2. Create `.env` using `example.com`:

   `cp example.com .env`

3. (Optional) change the values of environment variables in `.env` file

4. Start the containers:

   `docker compose up -d`

## Dependencies

Make sure all dependencies are up-to-date in case this repository
is not.

Those dependencies include:

- packages in [requirements](requirements)
- Docker images ([docker-compose.yml](docker-compose.yml)
  and [Dockerfile](Dockerfile))
- projects under `uses` keyword in
  [.github/workflows/release.yml](.github/workflows/release.yml)

