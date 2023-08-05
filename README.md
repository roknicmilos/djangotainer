# djangotainer

Steps for creating and setting up a
new Django project from this template:

1. Create a new directory for the project:

   `mkdir my_project`
    (replace `my_project` with the name of your project)

2. and go to that directory:

   `cd my_project`

3. Create virtual environment:

   `python3 -m venv venv`

4. Activate virtual environment:

   `source venv/bin/activate`

5. Install Django:

   `pip install django`

6. Create new Django project:

   `django-admin startproject --template https://github.com/roknicmilos/djangotainer/archive/main.zip my_project .`

7. Install default requirements:

   `pip install -r requirements.txt`

8. Run migrations:

   `python manage.py migrate`

9. Start development server:

   `python manage.py runserver`

## Preinstalled apps

### users

App `users`:
- comes with custom `User` model
- deactivates model admin for `Group` model

### common

App `common` comes with:

- models: `BaseModel` and `SingletonModel`
- management command: `load_data`
- custom base model admin classes (mixins)

## Default packages

These packages are defined in requirements.txt, and
they should be installed when setting up a project
using this Django project template.
