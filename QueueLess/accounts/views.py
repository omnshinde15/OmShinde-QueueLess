from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect("admin_dashboard")

        if request.user.is_staff:
            return redirect("staff_dashboard")

        return redirect("services")

    return redirect("login")


def login_view(request):

    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect("admin_dashboard")

        if request.user.is_staff:
            return redirect("staff_dashboard")

        return redirect("services")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Admin
            if user.is_superuser:
                return redirect("admin_dashboard")

            # Staff
            if user.is_staff:
                return redirect("staff_dashboard")

            # Normal customer
            return redirect("services")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "accounts/login.html")


def register_view(request):

    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect("admin_dashboard")

        if request.user.is_staff:
            return redirect("staff_dashboard")

        return redirect("services")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Passwords do not match."
                }
            )

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Username already exists."
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("services")

    return render(request, "accounts/register.html")


def logout_view(request):

    logout(request)

    return redirect("login")