import os

from django.core.wsgi import get_wsgi_application
from siecom.utils import get_environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"siecom.settings.{get_environment()}")

application = get_wsgi_application()
