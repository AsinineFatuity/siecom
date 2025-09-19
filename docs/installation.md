## Siecom Stores
A django-graphql microservice to model simple store operations
### Running The Project 
* Root directory refers to the location where `manage.py` file is

1. Run `git clone` on your local directory
2. Install `uv` tool from this link https://docs.astral.sh/uv/getting-started/installation/
3. Create a new virtual environment by running `uv venv .venv` in your root directory
4. Activate the environment by running `source .venv/bin/activate`
5. Install packages using the command `uv sync`
6. Create a `.env` file in your root directory and populate per `.env.example`
7. Create a local postgres db for app functioning and update `DATABASE_URL` in `.env` file accordingly
  * We use [dj-database-url](https://pypi.org/project/dj-database-url/) to configure django database values
8. Run migrations `python manage.py migrate`
9. Run `python3 manage.py runserver` to run the backend