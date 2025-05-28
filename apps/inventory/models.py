from django.db import models
from django.core.exceptions import ValidationError
from apps.products.models import Product
from apps.warehouses.models import Warehouse

class Stock(models.Model):
    class Meta:
        db_table = 'tbl_stocks'
        unique_together = ('product', 'warehouse')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=0)
    opening_stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_quantity(self, delta):
        new_quantity = self.quantity + delta
        if new_quantity < 0:
            raise ValidationError("Stock cannot go below zero.")
        self.quantity = new_quantity

        # Update max_quantity only if it's a stock-in and exceeds previous max
        if delta > 0 and self.quantity > self.max_quantity:
            self.max_quantity = self.quantity

        self.save()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"
    
    @property
    def display_stock(self):
        return self.opening_stock
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.product.low_stock_threshold

class StockLog(models.Model):
    STOCK_TYPE_CHOICES = [
        ('in', 'Stock-In'),
        ('out', 'Stock-Out'),
        ('adjust', 'Adjustment'),
        ('return', 'Return'),
    ]

    class Meta:
        db_table = 'tbl_stock_logs'

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    change = models.IntegerField()
    type = models.CharField(max_length=7, choices=STOCK_TYPE_CHOICES)
    reason = models.CharField(max_length=255, blank=True, null=True)
    reference_type = models.CharField(max_length=50, blank=True, null=True)
    reference_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validate consistency between change and type
        if self.type in ['in', 'return'] and self.change <= 0:
            raise ValidationError("Stock-In or Return must have a positive change.")
        if self.type in ['out'] and self.change >= 0:
            raise ValidationError("Stock-Out must have a negative change.")
        if self.type == 'adjust' and self.change == 0:
            raise ValidationError("Adjustment must have a non-zero change.")

    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.stock.update_quantity(self.change)

    def __str__(self):
        return f"{self.get_type_display()} {self.change} for {self.stock.product.name}"