from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
from django.db import models

# Create your models here.
class Person(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

class Documents(models.Model):
    CHOICES = (
        ('category1', 'category1'),
        ('category2', 'category2'),
        ('category3', 'category3'),
        ('category4', 'category4'),
        ('category5', 'category5'),
        ('category6', 'category6'),
        ('category7', 'category7'),
        ('category8', 'category8'),
        ('category9', 'category9'),
        ('category10', 'category10'),
        ('category11', 'category11'),
        ('category12', 'category12'),
    )
    type = models.CharField(max_length=500, choices=CHOICES)
    firstname=models.CharField(max_length=250)
    middlename=models.CharField(max_length=250)
    lastname=models.CharField(max_length=250)
    address=models.CharField(max_length=500)
    pincode=models.IntegerField(null=True)
    mobile=models.IntegerField(null=True)
    title = models.CharField(max_length=250,null=True)
    artist = models.CharField(max_length=250,null=True)
    place=models.CharField(max_length=250,null=True)
    created_by=models.ForeignKey(Person,on_delete=models.CASCADE,related_name="task_created_by",null=True, blank=True)

    def __str__(self):
        return self.type