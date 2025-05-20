from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdminUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

class AdminUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    # Add other fields as needed

    USERNAME_FIELD = 'username'
    objects = AdminUserManager()