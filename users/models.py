import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, RC_username, RC_password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        user = self.model(email=email, RC_username=RC_username, RC_password=RC_password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, RC_username=None, RC_password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, RC_username, RC_password, **extra_fields)

    def create_superuser(self, email, password, RC_username, RC_password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, RC_username, RC_password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    full_name = models.CharField(max_length=1024,)
    email = models.EmailField(unique=True)
    revel_est_id = models.CharField(max_length=128)
    company_name = models.CharField(max_length=256)
    RC_username = models.CharField(max_length=50, default="null")
    RC_password = models.CharField(max_length=50, default="null")

    is_staff = models.BooleanField(
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"

    objects = UserManager()


class LcOrderEmail(models.Model):
    email = models.EmailField(unique=True)
