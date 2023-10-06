# djangotainer

---

Table of Contents
=================

* [Quickstart](#quickstart)
    * [Create a new Django project](#create-a-new-django-project)
    * [Start the project](#start-the-project)
* [entrypoint.sh](#entrypointsh)
* [Preinstalled Django apps](#preinstalled-django-apps)
* [Default packages](#default-packages)
* [Dependencies](#dependencies)
* [Tests](#tests)
    * [Run tests](#run-tests)
    * [Run tests with coverage](#run-tests-with-coverage)
    * [Generate tests coverage report](#generate-tests-coverage-report)
* [Making changes](#making-changes)

___

## Quickstart

### Create Django project

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

### Start the project

If you created a Django project by following the steps from the
[Create a new Django project](#create-a-new-django-project) section,
you should now be able to start that Django project by following the
next steps:

1. Move to newly created Djagno project:

   `cd [my_project]`

2. Create `.env` using `example.com`:

   `cp example.com .env`

3. (Optional) change the values of environment variables in `.env` file

4. Start the containers:

   `docker compose up -d`

## entrypoint.sh

There is `entrypoint.sh` scripts in `django` container with multiple
options.

Run the script:

    docker compose run --rm django sh /app/scripts/entrypoint.sh [option]

Available options:

- ### `start`

  First, it connects the Django app to the database, and then
  it sets up necessary things for the Django app (static files,
  migrations, staff users, etc.).
  Finally, it starts the web server.

- ### `test`

  It runs tests with [Pytest](https://docs.pytest.org/)
  and [Coverage](https://coverage.readthedocs.io/).
  Tests will fail if specified coverage percentage is not
  satisfied.
  That coverage percentage is defined with environment
  variable `TEST_COVERAGE_PERCENTAGE` and it defaults to `100`.

## Preinstalled Django apps

This Django project template comes with three custom apps:
`common`, `users` and `emails`.

You can modify, extend or remove these apps if you want,
but note that they come with some minimal boilerplate code
that is quite common across majority of Django projects.

### `common` app

- models: `BaseModel` and `SingletonModel`
  - comes with `created` and `modified` fields, and `update` method
- management command: `load_data`
  - an extension of `loaddata` management command that
    already comes with standard Django project
  - this extension allows defining `FIXTURES` collection
    (`list` or `tuple`) in project `settings` that will be used to
    load the fixtures in a specific order defined by that collection
- custom model admin class (mixin)
  - easily separate fields (and fieldsets) for "add" and "change"
    model admin form
  - automatically adds readonly `ID` field that will be displayed at
    the top of the model admin form

### `users` app

- models: `User`
  - Django documentation [highly recommends setting up a
    custom user model](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
- deactivates model admin for `Group` model
  - to simplify the Django Admin interface by hiding `Group`
    model that is not that often used in Django projects

### `emails` app:

- models: `EamilThread`
  - Stores relevant email data and has functionality to send an
    email via `threading.Thread`
- `templates/example_email.html`
  - An email template example that can be used for custom email
    templates

## Default packages

When you create a new Django project using this project template,
some Python packages will be automatically installed when Docker
image for the Django project is built.

You can find these packages in [requirements](requirements) directory.

## Dependencies

Make sure all dependencies are up-to-date in case this repository
is not.

Those dependencies include:

- packages in requirements
- Docker images ([docker-compose.yml](docker-compose.yml)
  and [Dockerfile](Dockerfile))
- projects under `uses` keyword in [.github/workflows/release.yml](.github/workflows/release.yml)

## Tests

### Run tests

    docker compose run --rm django sh -c 'pytest'

The above command will run all tests.
Flag `-t` is optional (it provides additional output coloring when used).

To run the same tests in parallel, append `-n auto` to the `pytest` command:

    docker compose run --rm django sh -c 'pytest -n auto'

### Run tests with coverage

    docker compose run --rm django sh -c 'pytest --cov -n auto'

This will run all tests in parallel with coverage report.
Running tests like this is necessary to generate the tests coverage report.

### Generate tests coverage report

    docker compose run --rm django sh -c 'coverage html'

This will generate html for the tests coverage report which is useful when trying
to find out exactly which code is not covered by tests.
You can simply open the generated `index.html` in your browser and explore all files
and places in those files which are covered, not covered and ignored by tests coverage.

If you don't want the html, and you just want to see the overall coverage report, you
can run:

    docker compose run --rm django sh -c 'coverage report'

This will print the coverage report generated the last time tests wer run with the
coverage ([Run tests with coverage](#run-tests-with-coverage)).

## Making changes

There is a useful script called [create_project.sh](scripts/create_project.sh)
that does all the steps from the [Create a new Django project](#create-a-new-django-project)
section, and optionally also runs the steps from [Start the project](#start-the-project)
section.

Instead of doing all the steps from [Create a new Django project](#create-a-new-django-project)
and [Start the project](#start-the-project) sections, you can
use [create_project.sh](scripts/create_project.sh) to do all those
steps for you.

Check the comments on the top of the script file to see what are the
necessary requirements and steps for running the script.
