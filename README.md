## Siecom Stores
A django-graphql microservice to model simple store operations
### Running The Project 
1. Run `git clone` on your local directory
2. Create a `.env` file in your root directory and populate per `.env.example`
3. Run `docker compose up --build` to spin up the docker containers
* We have the following services:
  - `web` for our django/graphql app
  - `pgdb` for the postgres database
  - `ngix` for our reverse proxy 
# Project Documentation

- [Installation](docs/installation.md)
- [Coding Conventions](docs/conventions.md)
- [Code Quality Enforcement](docs/codequality.md)
- [Tests](docs/tests.md)
