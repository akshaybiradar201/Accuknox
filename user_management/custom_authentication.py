from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows login using email.
    """

    def authenticate(
        self,
        request: HttpRequest,
        username: str | None = ...,
        password: str | None = ...,
        **kwargs: Any
    ) -> AbstractBaseUser | None:
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass
        return None

    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
