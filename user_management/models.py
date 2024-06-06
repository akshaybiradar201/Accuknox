from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from user_management.managers import CustomUserManager


class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField("self", symmetrical=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def update_friend_count(self):
        self.num_friends = self.friends.count()
        self.save()


class Request(models.Model):
    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="sent_requests"
    )
    receiver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="received_requests"
    )

    class Meta:
        unique_together = (("sender", "receiver"),)
