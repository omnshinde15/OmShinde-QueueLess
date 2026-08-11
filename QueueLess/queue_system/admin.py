from django.contrib import admin
from .models import Service, Counter, Token


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "average_service_time",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service",
        "staff",
        "is_active",
    )
    list_filter = ("service", "is_active")
    search_fields = ("name",)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        "token_number",
        "user",
        "service",
        "counter",
        "status",
        "created_at",
    )
    list_filter = ("status", "service")
    search_fields = ("user__username",)