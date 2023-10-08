# Development corner

This project  includes a collection of handy scripts and Python
packages that streamline and enhance the development process.
The details and usage instructions for these scripts and Python
packages are described in the sections below.

## Making changes

Script `scripts/create_project.sh` does all the steps required for
creating a new Django project from
[djangotainer](https://github.com/roknicmilos/djangotainer)
template, and optionally also runs the steps starting that newly
created Django project.
Check the comments on the top of the script file to see what are the
necessary requirements and steps for running the script.

## entrypoint.sh

**NOTE:** Before running this script in the way described below,
make sure you are located in the root directory of the Django
project and that the `.env` file exists and has all the necessary
environment variables.

Run the script:

    docker compose run --rm django sh /app/scripts/entrypoint.sh [option]

### Available script options:

- ### `start`

  First, it connects the Django app to the database, and then
  it sets up necessary things for the Django app (static files,
  migrations, staff users, etc.).
  Finally, it starts the web server.

- ### `test`

  It runs tests with [Pytest](https://docs.pytest.org/) and
  [Coverage](https://coverage.readthedocs.io/).
  Tests will fail if specified coverage percentage is not
  satisfied.
  That coverage percentage is defined with environment variable
  `TEST_COVERAGE_PERCENTAGE` and it defaults to `100`.
  Check `src/pyproject.toml` for the Pytest and Coverage configuration.

- ### `check`

  Runs [Flake8](https://flake8.pycqa.org/) and
  [isort](https://pycqa.github.io/isort/), and throws an error if
  there are any issues in the code found by these tools.
  Check `src/pyproject.toml` for the Flake8 and isort configuration.

## Testing

This project uses [Pytest](https://docs.pytest.org/) for testing the
code and [Coverage](https://coverage.readthedocs.io/) for measuring
how much code has been covered by tests.

**NOTE:** Before running any of the commands mentioned below,
make sure you are located in the root directory of the Django
project and that the `.env` file exists and has all the necessary
environment variables.

### Run tests

    docker compose run --rm django sh -c 'pytest'

The above command will run all tests.
Flag `-t` is optional (it provides additional output coloring when used).

To run the same tests in parallel, append `-n auto` to the `pytest` command:

    docker compose run --rm django sh -c 'pytest -n auto'

### Run tests with coverage

    docker compose run --rm django sh -c 'pytest --cov -n auto'

This will run all tests in parallel with coverage report.
Running tests like this is necessary to generate the tests coverage
report.

### Generate tests coverage report

    docker compose run --rm django sh -c 'coverage html'

This will generate html for the tests coverage report which is useful when
trying to find out exactly which code is not covered by tests.
You can simply open the generated `index.html` in your browser and explore
all files and places in those files which are covered, not covered and
ignored by tests coverage.

If you don't want the html, and you just want to see the overall coverage
report, you can run:

    docker compose run --rm django sh -c 'coverage report'

This will print the coverage report generated the last time tests were run
with the coverage ([Run tests with coverage](#run-tests-with-coverage)).
