## Unit & Integration Tests
* We use [pytest-django](https://pytest-django.readthedocs.io/en/latest/) to create and run tests
* We use [factory-boy](https://factoryboy.readthedocs.io/en/stable/) to create dummy database objects
* Run tests using 

  a. `pytest -s` the `-s` flag is important in case you have a print statement in your test

  b. The `--reuse-db` is useful if you don't need to run migrations and recreate the schema

  c. We have installed [pytest-xdist](https://pypi.org/project/pytest-xdist/) to run tests in parallel. This makes tests run upto 2x faster. Use `pytest -n auto` with any of the other flags to experience this.
* More flags can be found in [pytest-documentation](https://docs.pytest.org/en/stable/how-to/index.html)

### Test Coverage
1. This project uses [coverage](https://coverage.readthedocs.io/en/7.6.1/) to gauge effectiveness of tests
2. To get a test coverage report:
   * Run `pytest -n auto --cov=.`
   * Generate report by running `pytest -n auto --cov=. --cov-report=term`