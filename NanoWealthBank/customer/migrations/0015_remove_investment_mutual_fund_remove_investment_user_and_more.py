# Generated by Django 5.1 on 2025-02-06 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_mutualfund_investment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='mutual_fund',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='user',
        ),
        migrations.DeleteModel(
            name='MutualFund',
        ),
        migrations.DeleteModel(
            name='Investment',
        ),
    ]
