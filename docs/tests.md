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
