from django.db import models

from accounts.models import User


class PurchaseStatus(models.TextChoices):
    NEW = "new", "NEW"
    ORDER = "order", "ORDER"
    SENT = "sent", "SENT"
    RECEIVED = "received", "RECEIVED"
    PROBLEM = "problem", "PROBLEM"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="грн")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_products")
    status = models.CharField(max_length=20, choices=PurchaseStatus.choices, default=PurchaseStatus.NEW)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="bought_products")
    solver_list = models.ManyToManyField(User, related_name="was_in_solver_list_for_products")
    final_solver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="was_solver_for_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


