





from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, username=None, admin_name=None, password=None, **extra_fields):
        """
        Create and save a regular User with the given email, username, and password.
        """
        if not username:
            raise ValueError('username must be set')

        user = self.model(
            username=username,
            admin_name=admin_name,
            **extra_fields
        )

        if email:
            user.email = email
        if username:
            user.username = username

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, admin_name=None, password=None, **extra_fields):
        """
        create superuser
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, admin_name, password, **extra_fields)



