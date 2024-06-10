# Generated by Django 5.0.6 on 2024-05-27 13:44

from django.db import migrations

def create_user(apps, schema_editor):
    User = apps.get_model('bank_management', 'User')
    User.objects.create(username='testuser', password='testpassword')

class Migration(migrations.Migration):

    dependencies = [
        ('bank_management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user),
    ]
