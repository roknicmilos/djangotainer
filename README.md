# djangotainer

## Quickstart:

---

### Create a new Django project

Below are the steps for creating a new Django project using the
[djangotainer](https://github.com/roknicmilos/djangotainer) project
template.

1. Create a new directory for the project:

   `mkdir my_project`
   (replace `my_project` with the name of your project)

2. Create Python virtual environment [venv](https://docs.python.org/3/library/venv.html) in the project directory:

   `python3 -m venv my_project/venv`

3. Activate Python virtual environment:

   `source my_project/venv/bin/activate`

4. Install Django:

   `pip install django`

5. Create new Django project from "djangotainer" project template:

   ```shell
    django-admin startproject --template djangotainer \
    --name=pyproject.toml,docker-compose.yml,example.env \
    my_project ./my_project
   ```

6. Deactivate and remove Python virtual environment:

   `deactivate && rm -rf my_project/venv`

### Start the project:

If you created a Django project by following the steps from the
[Create a new Django project](#create-a-new-django-project) section,
you should now be able to start that Django project by following the
next steps:

1. Move to newly created Djagno project:

   `cd my_project`

2. Create `.env` using `example.com`:

   `cp example.com .env`

3. (Optional) change the values of environment variables in `.env` file

4. Start the containers:

   `docker compose up -d`

## Preinstalled Django apps

This Django project template comes with two custom apps
(`users` and `common`).

You can modify, extend or remove these apps if you want,
but note that they come with some minimal boilerplate code
that is quite common across majority of Django projects.

`users` app:

- comes with custom `User` model
  - Django documentation [highly recommends setting up a
    custom user model](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
- deactivates model admin for `Group` model
  - to simplify the Django Admin interface by hiding `Group`
    model that is not that often used in Django projects

`common` app comes with:

- models: `BaseModel` and `SingletonModel`
  - comes with `created` and `modified` fields, and `update` method
- management command: `load_data`
  - an extension of `loaddata` management command that
    already comes with standard Django project
  - this extension allows defining `FIXTURES` collection
    (`list` or `tuple`) in project `settings` that will be used to
    load the fixtures in a specific defined by that collection
- custom model admin class (mixin)
  - easily separate fields (and fieldsets) for "add" and "change"
    model admin form
  - automatically adds readonly `ID` field that will be displayed at
    the top of the model admin form

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

## Making changes

There is a useful script called [create_project.sh](scripts/create_project.sh)
that does all the steps from the [Create a new Django project](#create-a-new-django-project)
section, and optionally also runs the steps from [Start the project](#start-the-project)
section.

When making changes to this project, it's necessary to check
if a new Django project can be created using this template.

Instead of doing all the steps from [Create a new Django project](#create-a-new-django-project)
and [Start the project](#start-the-project) sections, you can
use [create_project.sh](scripts/create_project.sh) to do all those
steps for you.

Check the comments on the top of the script file to see what are the
necessary requirements and steps for running the script.
