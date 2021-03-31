from django.db import models

from accounts.models import User


class PurchaseStatus(models.TextChoices):
    NEW = "new", "NEW"
    PENDING_ORDER = "pending_order", "PENDING ORDER"
    ORDER = "order", "ORDER"
    PENDING_SEND = "pending_send", "PENDING SEND"
    SENT = "sent", "SENT"
    PENDING_RECEIVED = "pending_received", "PENDING RECEIVED"
    RECEIVED = "received", "RECEIVED"
    PENDING_PROBLEM = "pending_problem", "PENDING_PROBLEM"
    PROBLEM = "problem", "PROBLEM"
    PENDING_REFUND = "pending_refund", "PENDING_REFUND"
    PENDING_NO_REFUND = "pending_no_refund", "PENDING_NO_REFUND"
    REFUND_BY_SOLVER = "refund", "REFUND_BY_SOLVER"
    NO_REFUND_BY_SOLVER = "no_refund", "NO_REFUND_BY_SOLVER"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="wei")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_products")
    status = models.CharField(max_length=20, choices=PurchaseStatus.choices, default=PurchaseStatus.NEW)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="bought_products")
    solver_list = models.ManyToManyField(User, related_name="was_in_solver_list_for_products")
    final_solver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="was_solver_for_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contract_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


