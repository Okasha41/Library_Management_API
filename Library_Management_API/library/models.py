from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(null=True, blank=True, default=None)
    total_copies = models.IntegerField()
    balance = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.title} by {self.author}'


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    date_of_membership = models.DateTimeField(auto_now_add=True)

    active_status = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('checked_out', 'Checked out'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
    ]
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='checked_out')

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date']

    def check_overdue(self):
        if self.status == 'checked_out' and self.due_date < now():
            self.status = 'overdue'
            self.save()

    def __str__(self):
        return f'{self.book.title} {self.transaction_type}'
