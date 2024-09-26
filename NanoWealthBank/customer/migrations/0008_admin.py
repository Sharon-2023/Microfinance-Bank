# Generated by Django 5.1 on 2024-09-26 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_customer_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
