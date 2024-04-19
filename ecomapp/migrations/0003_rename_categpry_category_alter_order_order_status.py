# Generated by Django 5.0.3 on 2024-03-28 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_product_image_alter_order_order_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categpry',
            new_name='Category',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Order Cancelled', 'Order Cancelled'), ('Order pending', 'Order Pending'), ('On the way', 'On the way'), ('Order Received', 'Order Received'), ('Order Completed', 'Order Completed')], max_length=50),
        ),
    ]