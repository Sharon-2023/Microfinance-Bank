# Generated by Django 5.1.1 on 2024-11-02 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0021_alter_transaction_purpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='user_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
