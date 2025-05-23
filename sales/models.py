from django.db import models
from django.utils.timezone import now
from django.db.models import Max
from users.models import User
from products.models import Product
from inventory.models import Stock
from warehouses.models import Warehouse
import uuid
from datetime import datetime

class Shift(models.Model):
    class Meta:
        db_table = 'tbl_shifts'

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='shifts')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    opened_at = models.DateTimeField(default=now)
    closed_at = models.DateTimeField(null=True, blank=True)
    opening_cash = models.DecimalField(max_digits=18, decimal_places=2)
    closing_cash = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    is_closed = models.BooleanField(default=False)


class Cart(models.Model):
    class Meta:
        db_table = 'tbl_carts'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class CartItem(models.Model):
    class Meta:
        db_table = 'tbl_cart_items'

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()


class Discount(models.Model):
    class Meta:
        db_table = 'tbl_discounts'

    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Transaction(models.Model):
    class Meta:
        db_table = 'tbl_transactions'

    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='transactions')
    transaction_number = models.CharField(max_length=20, unique=True, editable=False)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_contact = models.CharField(max_length=20, blank=True, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    change_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    payment_type = models.CharField(max_length=50, blank=False)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_number:
            date_part = datetime.now().strftime("%Y%m%d")
            random_part = uuid.uuid4().hex[:6].upper()  
            self.transaction_number = f"TRN-{date_part}-{random_part}"
        super().save(*args, **kwargs)

    def update_totals(self):
        
        subtotal = sum(item.get_total_price() for item in self.items.all())
        self.subtotal = subtotal

        if self.discount:
            self.discount_amount = (self.subtotal * self.discount.percentage) / 100
        else:
            self.discount_amount = 0

        self.total_amount = self.subtotal - self.discount_amount
        self.save(update_fields=['subtotal', 'discount_amount', 'total_amount'])

    def set_change_amount(self, amount_paid):
        self.change_amount = max(amount_paid - self.total_amount, 0)
        self.save(update_fields=['change_amount'])


class TransactionItem(models.Model):
    class Meta:
        db_table = 'tbl_transaction_items'

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk and not self.price_at_sale:
            self.price_at_sale = self.product.selling_price

        # Deduct stock on first save
        if not self.pk:
            stock = Stock.objects.get(product=self.product, warehouse=self.transaction.shift.warehouse)
            if stock.quantity < self.quantity:
                raise ValueError(f"Not enough stock for {self.product.product_name} in warehouse {self.transaction.shift.warehouse.name}")
            stock.quantity -= self.quantity
            stock.save()

        super().save(*args, **kwargs)

        # Update transaction totals
        self.transaction.update_totals()

    def get_total_price(self):
        return self.quantity * self.price_at_sale