# Generated by Django 4.2.2 on 2024-09-06 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_app', '0005_remove_module_description_remove_module_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='ordering_number',
            field=models.PositiveSmallIntegerField(verbose_name='порядковый номер'),
        ),
    ]
