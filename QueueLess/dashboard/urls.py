from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.staff_dashboard,
        name="staff_dashboard"
    ),

    path(
        "call-next/<int:counter_id>/",
        views.call_next,
        name="call_next"
    ),

    path(
        "complete/<int:token_id>/",
        views.complete_token,
        name="complete_token"
    ),

    path(
        "skip/<int:token_id>/",
        views.skip_token,
        name="skip_token"
    ),
]