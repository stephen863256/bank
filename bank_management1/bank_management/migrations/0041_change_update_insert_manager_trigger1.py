# Generated by Django 5.0.6 on 2024-06-10 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_management', '0040_change_update_insert_manager_trigger'),
    ]

    operations = [
        migrations.RunSQL("""
            DROP TRIGGER IF EXISTS update_manager_trigger;
            DROP TRIGGER IF EXISTS insert_manager_trigger;
        """),
    ]
