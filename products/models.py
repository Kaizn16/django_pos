from django.db import models

# Create your models here.
class Category(models.Model):
    class Meta:
        db_table = 'tbl_categories'

    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    class Meta:
        db_table = 'tbl_products'
    
    product_image = models.ImageField(null=True, default='', blank=True, upload_to='products/')
    product_name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    selling_price = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    buying_price = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(null=False, default=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name