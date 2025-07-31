from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

import os


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email
    

class Car(models.Model):

    STATUS_CHOICES = [
        ('purchased', 'Purchased'),
        ('repaired', 'Repaired'),
        ('sold', 'Sold'),
    ]

    
    name = models.CharField(max_length=255)
    price = models.BigIntegerField()
    photo = models.ImageField(upload_to="cars")
    specs = models.FileField(upload_to="specs")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='purchased')


    def delete(self, *args, **kwargs):
        print("delete method is called. ")
        # Delete associated files
        if self.photo and os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        if self.specs and os.path.isfile(self.specs.path):
            os.remove(self.specs.path)
        super().delete(*args, **kwargs)


