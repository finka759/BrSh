# Generated by Django 4.2.2 on 2024-09-23 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_merge_0002_alter_user_phone_0005_alter_payment_summ'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code_confirm',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='code_confirm'),
        ),
    ]
