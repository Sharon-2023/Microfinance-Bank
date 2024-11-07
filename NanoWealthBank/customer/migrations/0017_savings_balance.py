# Generated by Django 5.1.1 on 2024-11-02 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0016_alter_savings_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='savings',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]