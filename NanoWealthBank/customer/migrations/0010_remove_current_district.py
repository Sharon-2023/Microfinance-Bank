# Generated by Django 5.1 on 2024-10-23 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_savings_account_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='current',
            name='district',
        ),
    ]