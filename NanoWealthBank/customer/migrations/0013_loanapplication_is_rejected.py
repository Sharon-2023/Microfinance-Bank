# Generated by Django 5.1 on 2025-02-03 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_loanapplication_has_missed_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
