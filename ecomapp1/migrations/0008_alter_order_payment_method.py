# Generated by Django 5.0.3 on 2024-08-17 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp1', '0007_alter_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('K', 'Khalti Payment')], default='K', max_length=1),
        ),
    ]