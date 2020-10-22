import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

TTYPE = [("CR", "Credit"), ("DR", "Debit")]
# user model
class Customer(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Wallet(models.Model):
    owned_by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    status = models.BooleanField(default=True)
    enabled_at = models.DateField(null=True)
    disabled_at = models.DateField(null=True)

    def deposit(self, value):
        self.balance += value
        self.save()

    def withdraw(self, value):
        # Balance check
        if value > self.balance:
            return False

        self.balance -= value
        self.save()
        return True

    def enable(self):
        self.status = True
        self.enabled_at = datetime.now()
        self.save()
        return self.status

    def disable(self):
        self.status = False
        self.disabled_at = datetime.now()
        self.save()
        return self.status


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=2, choices=TTYPE)
    reference_id = models.CharField(max_length=100, unique=True)
    amount = models.FloatField()
    at = models.DateField()
