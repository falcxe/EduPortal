from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)
    yandex_id = models.CharField(max_length=200, blank=True, null=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"