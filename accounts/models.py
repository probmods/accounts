from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from custom_user.models import AbstractEmailUser
from django.utils import timezone
from django.core.mail import send_mail
import datetime
from django.utils import timezone
from django.conf import settings

# Create your models here.
class PmcUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves an EmailUser with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = PmcUserManager.normalize_email(email)
        user = self.model(email=email, is_staff=False, is_active=True,
                          is_superuser=False, last_login=now,
                          date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
class PmcUser(AbstractEmailUser):
    institution = models.CharField(max_length=70)
    education_status = models.CharField(max_length=70) 
    name = models.CharField(max_length=70, null=True)
    
    REQUIRED_FIELDS = ['institution', 'education_status']
    
