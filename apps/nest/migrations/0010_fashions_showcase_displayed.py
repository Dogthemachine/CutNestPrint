# Generated by Django 3.1.5 on 2021-08-02 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0009_auto_20210727_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='fashions',
            name='showcase_displayed',
            field=models.BooleanField(default=True, verbose_name='showcase_displayed'),
        ),
    ]
