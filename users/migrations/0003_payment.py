# Generated by Django 4.2.2 on 2024-09-14 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content_app', '0018_subscription'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='дата оплаты')),
                ('payment_method', models.CharField(blank=True, choices=[('CARD', 'картой'), ('CASH', 'наличными')], max_length=50, null=True, verbose_name='способ оплаты')),
                ('payment_link', models.URLField(blank=True, max_length=400, null=True, verbose_name='ссылка для оплаты')),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='идентификатор платежа')),
                ('summ', models.PositiveIntegerField(default=100, verbose_name='сумма платежа')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content_app.course', verbose_name='оплаченный курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
            },
        ),
    ]
