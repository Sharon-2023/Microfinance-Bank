# Generated by Django 5.1 on 2025-03-13 17:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0022_kycverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='current',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='fixeddeposit',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='savings',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterModelTable(
            name='current',
            table='current_account',
        ),
        migrations.AlterModelTable(
            name='fixeddeposit',
            table='fixed_deposit',
        ),
        migrations.AlterModelTable(
            name='savings',
            table='savings_account',
        ),
        migrations.AlterModelTable(
            name='transaction',
            table='transaction',
        ),
        migrations.DeleteModel(
            name='KYCVerification',
        ),
    ]
