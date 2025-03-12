from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


ROLE = (
    ('Administrator', 'Administrator'),
    ('Employee', 'Employee'),
    ('User', 'User'),
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class Basemodel(AbstractBaseUser):
    full_name = models.CharField(max_length=150)
    image_user = models.ImageField(upload_to='image_user/', null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, choices=ROLE)
    date_registered = models.DateField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f'{self.full_name}-{self.role}'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class UserProfile(Basemodel): # Регистрация для директора
    position = models.CharField(max_length=150)
    name_company = models.CharField(max_length=32)
    registration_number_company = models.PositiveSmallIntegerField()
    address_company = models.TextField()
    industry = models.TextField()

    def __str__(self):
        return f'{self.full_name}-{self.position}'

    class Meta:
        verbose_name_plural = "Директор"


class UserSimple(Basemodel):  # Регистрация для обычных пользователей
    pass

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Обычный пользователь"



class Openings(models.Model):
    opening_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class OpeningsTwo(Openings):
    pass


class OpeningsSree(Openings):
    pass

