# Generated by Django 5.1.1 on 2024-10-29 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_remove_customer_pin_customer_pin_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanOfficer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
