from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Expense(models.Model):
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    user = models.ForeignKey(User, related_name='user_whose_expense', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
