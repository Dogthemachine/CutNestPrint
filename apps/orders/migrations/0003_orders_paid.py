# Generated by Django 3.1.5 on 2021-09-08 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210908_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Paid or not'),
        ),
    ]
