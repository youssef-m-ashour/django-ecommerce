from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Egyptian mobile numbers: start with 01 followed by 0/1/2/5, then 8 digits.
# Examples: 01012345678, 01123456789, 01234567890, 01512345678
egyptian_phone_validator = RegexValidator(
    regex=r'^01[0125][0-9]{8}$',
    message="Enter a valid Egyptian mobile number, e.g. 01012345678."
)


class CustomUser(AbstractUser):
    """
    Custom user that logs in with email instead of username.
    We keep 'username' from AbstractUser (auto-filled from email) so that
    admin / createsuperuser and Django's permission system keep working.
    """
    email = models.EmailField(unique=True)
    mobile_phone = models.CharField(
        max_length=11,
        validators=[egyptian_phone_validator],
        help_text="Egyptian mobile number, e.g. 01012345678"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'mobile_phone']

    def __str__(self):
        return self.email
