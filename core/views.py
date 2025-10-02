import redis
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpRequest


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Welcome to Siecom Stores!"
        return context


def health_check(request: HttpRequest) -> JsonResponse:
    checks = {}
    status_code = 200
    try:
        db_conn = connections["default"]
        db_conn.cursor()
        checks["database"] = "ok"
    except OperationalError:
        checks["database"] = "error"
        status_code = 503
    try:
        cache.set("test", "test", timeout=10)
        value = cache.get("test")
        if value != "test":
            checks["cache"] = "error"
            status_code = 503
        else:
            checks["cache"] = "ok"
    except Exception as e:
        checks["cache"] = f"error: {e}"
        status_code = 503
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            socket_connect_timeout=10,
        )
        r.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {e}"
        status_code = 503
    checks["status"] = status_code
    response_dict = {
        "status": "ok" if status_code == 200 else "error",
        "message": "Health check completed",
        "checks": checks,
    }
    return JsonResponse(response_dict, status=status_code)
