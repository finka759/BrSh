# Generated by Django 4.2.2 on 2024-09-04 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, help_text='укажите ваш телефон', max_length=35, null=True, verbose_name='телефон'),
        ),
    ]
