from decouple import config

PROD_ENVIRONMENT = "production"
DEV_ENVIRONMENT = "development"


def get_environment():
    return config("ENVIRONMENT", default=PROD_ENVIRONMENT)
