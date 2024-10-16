# Generated by Django 5.1 on 2024-10-09 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Savings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('account_type', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
            ],
        ),
    ]
