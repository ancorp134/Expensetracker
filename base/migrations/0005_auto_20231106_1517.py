# Generated by Django 3.2.22 on 2023-11-06 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_expense_departure'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='taxi_bill',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='taxi_bill_proof',
        ),
    ]