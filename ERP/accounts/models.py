from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Division(models.Model):
    DIVISION_CHOICES = [
        ('AMERICAN', 'American'),
        ('BRITISH', 'British'),
        ('FRENCH', 'French'),
    ]
    name = models.CharField(max_length=20, choices=DIVISION_CHOICES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.SUPER_ADMIN)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    SUPER_ADMIN = 'SUPER_ADMIN'
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    ACCOUNTANT = 'ACCOUNTANT'
    STAFF = 'STAFF'
    PARENT = 'PARENT'

    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (ACCOUNTANT, 'Accountant'),
        (STAFF, 'Staff'),
        (PARENT, 'Parent'),
    ]

    username   = models.CharField(max_length=150, unique=True)
    email      = models.EmailField(unique=True)
    full_name  = models.CharField(max_length=200)
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STAFF)
    division   = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='users')
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        return self.role == self.SUPER_ADMIN

    @property
    def is_admin_role(self):
        return self.role in (self.SUPER_ADMIN, self.ADMIN)

    @property
    def is_teacher(self):
        return self.role == self.TEACHER

    @property
    def is_accountant(self):
        return self.role == self.ACCOUNTANT
