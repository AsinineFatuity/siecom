from django.contrib import admin
from core.models import User, Category, Product, Order

admin.site.site_title = "Siecom Admin"
admin.site.site_header = "Siecom Administration"
admin.site.index_title = "Admin Portal"


@admin.register(User)
@admin.register(Category)
@admin.register(Product)
@admin.register(Order)
class BaseAdmin(admin.ModelAdmin):
    pass
