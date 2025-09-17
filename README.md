## Siecom Stores
A django microservice to model simple store functionalities as an excuse to explore complex devops concepts

### Running The Project 
* Root directory refers to the location where `manage.py` file is

1. Run `git clone` on your local directory
2. Install `uv` tool from this link [https://docs.astral.sh/uv/getting-started/installation/]
3. Create a new virtual environment by running `uv venv .venv` in your root directory
4. Activate the environment by running `source .venv/bin/activate`
5. Install packages using the command `uv sync`
6. Create a `.env` file in your root directory and populate per `.env.example`
7. Create a local postgres db for app functioning and update `DATABASE_URL` in `.env` file accordingly
  * We use [dj-database-url](https://pypi.org/project/dj-database-url/) to configure django database values
8. Run migrations `python manage.py migrate`
9. Run `python3 manage.py runserver` to run the backend

## Code Quality
1. This project uses [ruff code formatter](https://docs.astral.sh/ruff/formatter/) to achieve consistency in formatting code in line with [PEP 8](https://peps.python.org/pep-0008/) standards
2. Whenever changes are made to code, run `ruff format` to format the changed files
3. Ruff also enforces `PEP8` standards and detects non conformant code through linting
4. Whenever changes are made to code, run `ruff check` to check for non comformant code
To easily enforce these standards, you can do the following 
* Go the `.git/hooks` folder and add create a `pre-commit` file then add the following
```bash 
#!/bin/sh

# Get the list of staged Python files
files=$(git diff --name-only --cached --diff-filter=d -- '*.py')

# If there are any Python files staged, format them with Ruff
if [ -n "$files" ]; then
    echo "Running ruff formatter on staged files..."
    ruff format $files

    # Add the formatted files back to staging
    git add $files
    echo "Running ruff linting tool on staged files..."
    ruff check $files
else
   echo "No staged files found to run ruff formatter on ..."
fi
```
This custom precommit hook will ensure that all changed files are linted and formatted when `git commit` is run
* Ensure you run `chmod +x .git/pre-commit` to make the script exec

## Coding Conventions
1. Django models mutations are encapsulated as per [this convention](https://github.com/octoenergy/public-conventions/blob/main/conventions/django.md#encapsulate-model-mutation)
2. For any new graphql schema endpoint implemented, the preferred folder structure is
   * `core/graphql/endpoint_name` as `base_directory`
   * `base_directory/mutations.py` where all mutations endpoints live
   * `base_directory/queries.py` where all queries endpoints live
   * `base_directory/types.py` where the shared object type between mutations and queries live
   * `base_directory/feedback.py` where all the related endpoint feedback live

As much as possible all feedback is written per [this convention](https://github.com/octoenergy/public-conventions/blob/main/conventions/django.md#flash-messages)
  
* See `api/graphql/user` for an example of this convention

3. For any models created, we obfuscate the incremental ids so that we don't send them to the frontend
   * We thus use a custom `CustomDjangoObjectType` class in `api/graphql/public_identifier` for any graphql type
   * New models should inherit the `AuditIdentifierMixin` from `api/models/abstract` that automatically adds a uuid4 `public_id` field that is unique to each instance upon creation
   * See `api/graphql/user` for an example of such implementation
4. For any new migrations use the `--name` flag to provide a descriptive name 

## Unit Tests
* We use [pytest-django](https://pytest-django.readthedocs.io/en/latest/) to create and run tests
* We use [factory-boy](https://factoryboy.readthedocs.io/en/stable/) to create dummy database objects
* Run tests using 

  a. `pytest -s` the `-s` flag is important in case you have a print statement in your test

  b. The `--reuse-db` is useful if you don't need to run migrations and recreate the schema

  c. We have installed [pytest-xdist](https://pypi.org/project/pytest-xdist/) to run tests in parallel. This makes tests run upto 2x faster. Use `pytest -n auto` with any of the other flags to experience this magic.
* More flags can be found in [pytest-documentation](https://docs.pytest.org/en/stable/how-to/index.html)