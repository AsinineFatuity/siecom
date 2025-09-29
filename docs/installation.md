## Running The Project 
### Set Up With Docker 
1. Run `git clone` on your local directory
2. Create a `.env` file in your root directory and populate per `.env.example`
3. Run `docker compose up --build` to spin up the docker containers
* We have the following services:
  - `web` for our django/graphql microservice
  - `pgdb` for the postgres database
  - `nginx` for our reverse proxy 
  - `huey` for background asynchronous task
  - `redis` for storing task queues
4. Navigate to `http://127.0.0.1:8080/` to confirm it is running successfully
5. All python commands to the `web` service will be prepended with `docker compose exec web` e.g `docker compose exec web python manage.py shell`
6. Run prepend `manage.py runscript init_db` to populate db with products

### Set Up Without Docker
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
9. Run `python manage.py runscript init_db` to populate db with products
10. Run `python manage.py runserver` to run the backend
11. Install redis on your system and run `python manage.py run_huey` to run the background task process
12. Navigate to `http://127.0.0.1:8000/` to confirm it is running successfully
