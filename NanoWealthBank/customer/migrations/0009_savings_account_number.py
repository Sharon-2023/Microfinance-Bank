# Generated by Django 5.1 on 2024-10-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_remove_savings_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='savings',
            name='account_number',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
