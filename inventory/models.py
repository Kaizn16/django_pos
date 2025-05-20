from django.db import models
from products.models import Product
from django.core.exceptions import ValidationError

# Create your models here.
class Stock(models.Model):
    class Meta:
        db_table = 'tbl_stocks'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Update max_quantity if current quantity exceeds it
    def save(self, *args, **kwargs):
        if self.quantity > self.max_quantity: 
            self.max_quantity = self.quantity
        super().save(*args, **kwargs)


class StockLog(models.Model):
    STOCK_TYPE_CHOICES = [
        ('in', 'Stock-In'),
        ('out', 'Stock-Out'),
    ]

    class Meta:
        db_table = 'tbl_stock_logs'

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False, blank=False)
    change = models.IntegerField()
    type = models.CharField(max_length=3, choices=STOCK_TYPE_CHOICES)
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Ensure consistency between `change` and `type`
        if self.type == 'in' and self.change < 0:
            raise ValidationError("Stock-In must have a positive change.")
        if self.type == 'out' and self.change > 0:
            raise ValidationError("Stock-Out must have a negative change.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
