# Generated by Django 5.0.6 on 2024-06-05 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_management', '0029_crdrop_event'),
    ]

    operations = [
        migrations.RunSQL('''
            DROP EVENT if exists update_interest;
        '''),
        migrations.RunSQL('''
            CREATE EVENT update_interest
            ON SCHEDULE EVERY 1 DAY STARTS CURRENT_TIMESTAMP
            DO
              UPDATE bank_management_creditaccount
              SET interest = CASE
                WHEN DATEDIFF(CURDATE(), lastRepaymentDate) > 30 THEN
                  (creditLimit - creditBalance) * interestRate * (DATEDIFF(CURDATE(), lastRepaymentDate) - 30)
                ELSE
                  0
              END;
        ''')
    ]
