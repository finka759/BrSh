# Generated by Django 4.2.2 on 2024-09-06 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content_app', '0006_alter_module_ordering_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='owner',
        ),
    ]
