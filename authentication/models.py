from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    user model for creating and storing users in db
    """
    username = models.CharField(max_length=250, unique=True, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        """
        save method to handle password encryption for non superuser
        """
        if self.is_superuser == False:
            if not self.pk:
                self.set_password(self.password)
        super().save(*args, **kwargs)
