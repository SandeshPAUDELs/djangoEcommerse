# Generated by Django 5.0.3 on 2024-04-21 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0005_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Order Received', 'Order Received'), ('On the way', 'On the way'), ('Order pending', 'Order Pending'), ('Order Cancelled', 'Order Cancelled'), ('Order Completed', 'Order Completed')], max_length=50),
        ),
    ]