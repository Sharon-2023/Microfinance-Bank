# Generated by Django 5.1 on 2024-10-25 10:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_remove_current_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('transfer', 'Transfer')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recipient_name', models.CharField(blank=True, max_length=100, null=True)),
                ('recipient_account', models.CharField(blank=True, max_length=100, null=True)),
                ('purpose', models.CharField(blank=True, max_length=200, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='customer.customer')),
            ],
        ),
    ]
