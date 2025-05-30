# Generated by Django 4.2.8 on 2025-05-28 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0001_initial'),
        ('products', '0001_initial'),
        ('warehouses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shifts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shift',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouses.warehouse'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sales.cart'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='shift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.shift'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
