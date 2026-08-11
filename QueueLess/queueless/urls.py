from django.contrib import admin
from django.urls import include, path

from accounts import views as account_views
from queue_system import views as queue_views
from dashboard import views as dashboard_views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", account_views.home, name="home"),

    path("login/", account_views.login_view, name="login"),
    path("register/", account_views.register_view, name="register"),
    path("logout/", account_views.logout_view, name="logout"),

    path("services/", queue_views.services, name="services"),
    path("token/", queue_views.generate_token, name="generate_token"),
    path("history/", queue_views.history, name="history"),

    path(
        "token/<int:token_id>/",
        queue_views.token_status,
        name="token_status",
    ),

    path(
        "staff/",
        include("dashboard.urls"),
    ),

    path(
        "dashboard/admin/",
        dashboard_views.admin_dashboard,
        name="admin_dashboard",
    ),
    path(
        "dashboard/admin/service/add/",
        dashboard_views.service_create,
        name="service_create",
    ),

    path(
        "dashboard/admin/service/<int:service_id>/edit/",
        dashboard_views.service_edit,
        name="service_edit",
    ),

    path(
        "dashboard/admin/service/<int:service_id>/toggle/",
        dashboard_views.service_toggle,
        name="service_toggle",
    ),
    path(
        "dashboard/admin/counter/add/",
        dashboard_views.counter_create,
        name="counter_create"
    ),

    path(
        "dashboard/admin/counter/<int:counter_id>/edit/",
        dashboard_views.counter_edit,
        name="counter_edit"
    ),

    path(
        "dashboard/admin/counter/<int:counter_id>/toggle/",
        dashboard_views.counter_toggle,
        name="counter_toggle"
    ),
]