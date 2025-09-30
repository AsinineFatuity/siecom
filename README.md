## Siecom Stores
[![Coverage Status](https://coveralls.io/repos/github/AsinineFatuity/siecom/badge.svg?branch=main)](https://coveralls.io/github/AsinineFatuity/siecom?branch=main)

A django-graphql microservice to model simple store operations

This microservice is deployed in kubernetes cluster at http://174.138.123.164/ with a CI/CD pipeline configured

### Features Overview
**OIDC Authentication**: The microservice uses OpenID Connect (OIDC) for authentication and authorization. It is implemented in a stateless way: instead of storing session data or issuing its own JWTs, the service validates incoming tokens directly against the OIDC provider’s public resources (such as the `.well-known configuration` and JSON Web Keys). This ensures that only users with valid OIDC-issued tokens can access the service.This exists at [this endpoint](docs/schema.md#mutation)

**Products & Product Categories**: The microservice exposes an [API endpoint](docs/schema.md#mutation) that allow authenticated users to create products and organize them into categories. Categories are structured as a hierarchical tree and can be nested beyond three levels, enabling complex product taxonomies.

Unauthenticated users can query all products using this [API endpoint](docs/schema.md#query)

**Average Category Price**: The microservice provides an [API endpoint](docs/schema.md#query) that allows all users to calculate the average price of products within a given category.

**Order Creation**: The microservice provides an [API endpoint](docs/schema.md#mutation) for authenticated users to create orders for selected products.

**Order Alerts**: The microservice notifies admins of new orders via email to support dispatch, and sends order confirmations to customers via SMS.

These features can be viewed with annotated screen shots [here](docs/results.md)

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

### Project Documentation
- [Installation](docs/installation.md)
- [Coding Conventions](docs/conventions.md)
- [Code Quality Enforcement](docs/codequality.md)
- [Tests](docs/tests.md)
- [Deployment](docs/deployment.md)
- [Graphql Api Documentation](docs/schema.md)
- [Results As Per Project Requirements](docs/results.md)
