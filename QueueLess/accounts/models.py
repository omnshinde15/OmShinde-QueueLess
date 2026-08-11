from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("CUSTOMER", "Customer"),
        ("STAFF", "Staff"),
        ("ADMIN", "Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="CUSTOMER"
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"