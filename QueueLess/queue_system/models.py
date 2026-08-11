from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    average_service_time = models.PositiveIntegerField(
        default=5,
        help_text="Average service time in minutes"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Counter(models.Model):
    name = models.CharField(max_length=50)
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="counters"
    )
    staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_counters"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.service.name}"


class Token(models.Model):
    STATUS_CHOICES = [
        ("WAITING", "Waiting"),
        ("SERVING", "Serving"),
        ("COMPLETED", "Completed"),
        ("SKIPPED", "Skipped"),
        ("CANCELLED", "Cancelled"),
    ]

    token_number = models.PositiveIntegerField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tokens"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="tokens"
    )

    counter = models.ForeignKey(
        Counter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tokens"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="WAITING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    called_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.service.name} - #{self.token_number}"