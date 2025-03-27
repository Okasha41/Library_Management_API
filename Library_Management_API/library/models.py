from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(null=True, blank=True, default=None)
    balance = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.title} by {self.author}'


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if not password:
            raise ValueError('Superuser must have a password')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('active_status', True)
        return self.create_user(username, email, password=None, **extra_fields)


class CustomeUserModel(AbstractBaseUser):
    # Required Fields
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    # Date of membership
    date_of_membership = models.DateTimeField(auto_now_add=True)

    # Active status
    active_status = models.BooleanField(default=True)

    # Additional fields for Django's admin functionality
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # specify the field used to login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # Custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff


class Transactions(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(
        CustomeUserModel, on_delete=models.CASCADE, related_name='transactions')
    TRANSACTION_CHOICES = [
        ('return', 'Return'),
        ('check_out', 'Check_out')
    ]
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_CHOICES)
    transaction_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [
        ('checked_out', 'Checked out'),
        ('returned', 'Returned'),
        ('over_due', 'Overdue')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date']
        unique_together = ['user', 'book']
