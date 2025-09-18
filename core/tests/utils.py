import random
from faker import Factory as FakerFactory

faker_factory = FakerFactory.create()


def format_list_items(items):
    """Allows sending of list items as a string e.g multiple ids"""
    return ", ".join(['"' + str(item) + '"' for item in items])


def generate_phone_with_country_code(country_code: str = "+254") -> str:
    local_number = "".join([str(random.randint(0, 9)) for _ in range(9)])
    return f"{country_code}{local_number}"


def boolean_to_string(value: bool) -> str:
    """Convert a boolean value to a string."""
    return "true" if value else "false"
