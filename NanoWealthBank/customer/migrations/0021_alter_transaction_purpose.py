# Generated by Django 5.1.1 on 2024-11-02 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_remove_transaction_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='purpose',
            field=models.TextField(blank=True, null=True, verbose_name='Purpose of Transfer'),
        ),
    ]