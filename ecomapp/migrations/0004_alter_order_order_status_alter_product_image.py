# Generated by Django 5.0.3 on 2024-03-31 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0003_rename_categpry_category_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('On the way', 'On the way'), ('Order Received', 'Order Received'), ('Order Completed', 'Order Completed'), ('Order pending', 'Order Pending'), ('Order Cancelled', 'Order Cancelled')], max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='media/products/default_image.png', upload_to='products'),
        ),
    ]
