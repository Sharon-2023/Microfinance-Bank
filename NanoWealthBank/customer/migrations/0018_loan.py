# Generated by Django 5.1.1 on 2024-11-02 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0017_savings_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=50)),
                ('nationality', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=100)),
                ('employment_status', models.CharField(choices=[('employed', 'Employed'), ('unemployed', 'Unemployed')], max_length=20)),
                ('monthly_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_certificate', models.FileField(upload_to='documents/salary_certificates/')),
                ('loan_type', models.CharField(choices=[('personal', 'Personal Loan'), ('vehicle', 'Vehicle Loan')], max_length=10)),
                ('loan_amount_required', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_purpose', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
    ]
