# Generated by Django 5.1 on 2024-09-25 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_rename_customer_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Customer',
        ),
    ]
