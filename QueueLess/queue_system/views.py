from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Service, Token


@login_required
def services(request):
    services_list = Service.objects.filter(is_active=True)

    return render(
        request,
        "queue/services.html",
        {
            "services": services_list,
        }
    )


@login_required
def generate_token(request):
    if request.method != "POST":
        return redirect("services")

    service_id = request.POST.get("service_id")

    service = get_object_or_404(
        Service,
        id=service_id,
        is_active=True
    )

    last_token = (
        Token.objects
        .filter(service=service)
        .order_by("-token_number")
        .first()
    )

    if last_token:
        next_token_number = last_token.token_number + 1
    else:
        next_token_number = 1

    token = Token.objects.create(
        token_number=next_token_number,
        user=request.user,
        service=service
    )

    return render(
        request,
        "queue/token.html",
        {
            "token": token,
        }
    )


@login_required
def history(request):
    tokens = (
        Token.objects
        .filter(user=request.user)
        .select_related("service", "counter")
        .order_by("-created_at")
    )

    return render(
        request,
        "queue/history.html",
        {
            "tokens": tokens,
        }
    )


@login_required
def token_status(request, token_id):
    token = get_object_or_404(
        Token,
        id=token_id,
        user=request.user
    )

    # People waiting before this customer
    people_ahead = Token.objects.filter(
        service=token.service,
        status="WAITING",
        created_at__lt=token.created_at
    ).count()

    # Estimated waiting time
    estimated_wait = (
        people_ahead * token.service.average_service_time
    )

    return render(
        request,
        "queue/token_status.html",
        {
            "token": token,
            "people_ahead": people_ahead,
            "estimated_wait": estimated_wait,
        }
    )