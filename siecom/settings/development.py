import os
from siecom.settings.base import *  # noqa: F403

ALLOWED_HOSTS = ["*"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# ssl settings
HOST_SCHEME = "http://"
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False
