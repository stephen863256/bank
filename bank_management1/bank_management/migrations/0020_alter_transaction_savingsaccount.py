# Generated by Django 5.0.6 on 2024-06-05 03:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_management', '0019_insert_transaction_triggers1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='savingsAccount',
            field=models.ForeignKey(db_column='accountId', on_delete=django.db.models.deletion.CASCADE, to='bank_management.savingsaccount'),
        ),
    ]
