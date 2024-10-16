# Generated by Django 5.1 on 2024-10-16 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_remove_savings_is_approved_remove_savings_is_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='account_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='savings',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='savings',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='SavingsAccountRequest',
        ),
    ]
