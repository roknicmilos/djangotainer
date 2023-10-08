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
- `Send selected emails` action in the list view for `EamilThread`
  model in Django Admin
- `templates/emails/base.html`
    - A base for custom emails templates
