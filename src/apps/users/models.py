from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class UserManager(BaseUserManager):
    # TODO: REMOVE "pragma: no cover" when tests for it are implemented
    def create_superuser(self, email: str = None, **kwargs):  # pragma: no cover
        return self._create_user(email=email, is_staff=True, is_superuser=True, **kwargs)

    # TODO: REMOVE "pragma: no cover" when tests for it are implemented
    def create_user(self, email: str = None, **kwargs):  # pragma: no cover
        return self._create_user(email=email, is_staff=False, is_superuser=False, **kwargs)

    # TODO: REMOVE "pragma: no cover" when tests for it are implemented
    def _create_user(self, email: str = None, password: str = None, **kwargs):  # pragma: no cover
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.update(password=make_password(password))
        return user


class User(BaseModel, AbstractUser):
    # TODO:
    #   1. configure PostgreSQL
    #   2. create migration for "case_insensitive" db_collation
    #   3. uncomment the code below
    #   3. create migration for the uncommented code
    # email = models.EmailField(
    #     verbose_name=_("email"),
    #     db_collation="case_insensitive",
    #     unique=True
    # )
    # username = None

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
