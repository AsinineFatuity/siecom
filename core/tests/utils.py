import datetime
from jose import jwt
from faker import Factory as FakerFactory

faker_factory = FakerFactory.create()


def format_list_items(items):
    """Allows sending of list items as a string e.g multiple ids"""
    return ", ".join(['"' + str(item) + '"' for item in items])


def generate_phone_with_country_code(country_code: str = "+254") -> str:
    local_number = "712345678"
    return f"{country_code}{local_number}"


def boolean_to_string(value: bool) -> str:
    """Convert a boolean value to a string."""
    return "true" if value else "false"


def make_oidc_token(exp_minutes=60) -> str:
    """Helper to mint JWTs for tests."""
    now = datetime.datetime.now()
    payload = {
        "sub": "google-oauth2|116335214551149049094",
        "email": "test@yopmail.com",
        "iat": now,
        "exp": now + datetime.timedelta(minutes=exp_minutes),
        "iss": "https://dev-xyz123.us.auth0.com",
        "aud": "https://dev-xyz123.us.auth0.com/api/v2/",
    }
    return jwt.encode(payload, "dummy_secret", algorithm="HS256")
