from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from queue_system.models import Counter, Service, Token


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required
def admin_dashboard(request):

    # Only superusers can access admin dashboard
    if not request.user.is_superuser:
        return redirect("services")

    services = Service.objects.all()

    counters = Counter.objects.select_related(
        "service",
        "staff"
    ).all()

    tokens = Token.objects.select_related(
        "user",
        "service",
        "counter"
    ).order_by("-created_at")

    # Dashboard statistics
    total_services = services.count()
    active_services = services.filter(
        is_active=True
    ).count()

    total_counters = counters.count()
    active_counters = counters.filter(
        is_active=True
    ).count()

    total_tokens = tokens.count()

    waiting_tokens = tokens.filter(
        status="WAITING"
    ).count()

    serving_tokens = tokens.filter(
        status="SERVING"
    ).count()

    completed_tokens = tokens.filter(
        status="COMPLETED"
    ).count()

    skipped_tokens = tokens.filter(
        status="SKIPPED"
    ).count()

    return render(
        request,
        "dashboard/admin.html",
        {
            "services": services,
            "counters": counters,
            "tokens": tokens,

            "total_services": total_services,
            "active_services": active_services,

            "total_counters": total_counters,
            "active_counters": active_counters,

            "total_tokens": total_tokens,
            "waiting_tokens": waiting_tokens,
            "serving_tokens": serving_tokens,
            "completed_tokens": completed_tokens,
            "skipped_tokens": skipped_tokens,
        }
    )


# =========================================================
# STAFF DASHBOARD
# =========================================================

@login_required
def staff_dashboard(request):

    # Only staff members can access staff dashboard
    if not request.user.is_staff or request.user.is_superuser:
        return redirect("services")

    counters = Counter.objects.filter(
        staff=request.user,
        is_active=True
    ).select_related("service")

    tokens = Token.objects.filter(
        counter__staff=request.user,
        status__in=["WAITING", "SERVING"]
    ).select_related(
        "user",
        "service",
        "counter"
    ).order_by("created_at")

    return render(
        request,
        "dashboard/staff.html",
        {
            "counters": counters,
            "tokens": tokens,
        }
    )


# =========================================================
# CALL NEXT TOKEN
# =========================================================

@login_required
def call_next(request, counter_id):

    # Staff only
    if not request.user.is_staff or request.user.is_superuser:
        return redirect("services")

    counter = get_object_or_404(
        Counter,
        id=counter_id,
        staff=request.user,
        is_active=True
    )

    token = Token.objects.filter(
        service=counter.service,
        status="WAITING"
    ).order_by("created_at").first()

    if token:
        token.status = "SERVING"
        token.counter = counter
        token.save()

    return redirect("staff_dashboard")


# =========================================================
# COMPLETE TOKEN
# =========================================================

@login_required
def complete_token(request, token_id):

    # Staff only
    if not request.user.is_staff or request.user.is_superuser:
        return redirect("services")

    token = get_object_or_404(
        Token,
        id=token_id,
        counter__staff=request.user
    )

    token.status = "COMPLETED"
    token.save()

    return redirect("staff_dashboard")


# =========================================================
# SKIP TOKEN
# =========================================================

@login_required
def skip_token(request, token_id):

    # Staff only
    if not request.user.is_staff or request.user.is_superuser:
        return redirect("services")

    token = get_object_or_404(
        Token,
        id=token_id,
        counter__staff=request.user
    )

    token.status = "SKIPPED"
    token.save()

    return redirect("staff_dashboard")


# =========================================================
# CREATE SERVICE
# =========================================================

@login_required
def service_create(request):

    # Admin only
    if not request.user.is_superuser:
        return redirect("services")

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        average_service_time = request.POST.get(
            "average_service_time"
        )

        Service.objects.create(
            name=name,
            description=description,
            average_service_time=average_service_time,
            is_active=True,
        )

        return redirect("admin_dashboard")

    return render(
        request,
        "dashboard/service_form.html",
        {
            "title": "Add Service",
            "button_text": "Add Service",
        }
    )


# =========================================================
# EDIT SERVICE
# =========================================================

@login_required
def service_edit(request, service_id):

    # Admin only
    if not request.user.is_superuser:
        return redirect("services")

    service = get_object_or_404(
        Service,
        id=service_id
    )

    if request.method == "POST":

        service.name = request.POST.get("name")

        service.description = request.POST.get(
            "description"
        )

        service.average_service_time = request.POST.get(
            "average_service_time"
        )

        service.save()

        return redirect("admin_dashboard")

    return render(
        request,
        "dashboard/service_form.html",
        {
            "title": "Edit Service",
            "button_text": "Save Changes",
            "service": service,
        }
    )


# =========================================================
# TOGGLE SERVICE
# =========================================================

@login_required
def service_toggle(request, service_id):

    # Admin only
    if not request.user.is_superuser:
        return redirect("services")

    service = get_object_or_404(
        Service,
        id=service_id
    )

    service.is_active = not service.is_active
    service.save()

    return redirect("admin_dashboard")


# =========================================================
# CREATE COUNTER
# =========================================================

@login_required
def counter_create(request):

    # Admin only
    if not request.user.is_superuser:
        return redirect("services")

    if request.method == "POST":

        name = request.POST.get("name")
        service_id = request.POST.get("service")
        staff_id = request.POST.get("staff")

        service = get_object_or_404(
            Service,
            id=service_id
        )

        staff = None

        if staff_id:

            staff = get_object_or_404(
                User,
                id=staff_id,
                is_staff=True,
                is_superuser=False
            )

        Counter.objects.create(
            name=name,
            service=service,
            staff=staff,
            is_active=True
        )

        return redirect("admin_dashboard")

    services = Service.objects.filter(
        is_active=True
    )

    staff_users = User.objects.filter(
        is_staff=True,
        is_superuser=False
    )

    return render(
        request,
        "dashboard/counter_form.html",
        {
            "title": "Add Counter",
            "button_text": "Add Counter",
            "services": services,
            "staff_users": staff_users,
        }
    )


# =========================================================
# EDIT COUNTER
# =========================================================

@login_required
def counter_edit(request, counter_id):

    # Admin only
    if not request.user.is_superuser:
        return redirect("services")

    counter = get_object_or_404(
        Counter,
        id=counter_id
    )

    if request.method == "POST":

        counter.name = request.POST.get(
            "name"
        )

        service_id = request.POST.get(
            "service"
        )

        staff_id = request.POST.get(
            "staff"
        )

        counter.service = get_object_or_404(
            Service,
            id=service_id
        )

        if staff_id:

            counter.staff = get_object_or_404(
                User,
                id=staff_id,
                is_staff=True,
                is_superuser=False
            )

        else:

            counter.staff = None

        counter.save()

        return redirect("admin_dashboard")

    services = Service.objects.filter(
        is_active=True
    )

    staff_users = User.objects.filter(
        is_staff=True,
        is_superuser=False
    )

    return render(
        request,
        "dashboard/counter_form.html",
        {
            "title": "Edit Counter",
            "button_text": "Save Changes",
            "counter": counter,
            "services": services,
            "staff_users": staff_users,
        }
    )


# =========================================================
# TOGGLE COUNTER
# =========================================================

@login_required
def counter_toggle(request, counter_id):

    # Admin only
    if not request.user.is_superuser:
        return redirect("services")

    counter = get_object_or_404(
        Counter,
        id=counter_id
    )

    counter.is_active = not counter.is_active
    counter.save()

    return redirect("admin_dashboard")