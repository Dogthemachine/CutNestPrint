# Generated by Django 3.1.5 on 2021-08-02 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0010_fashions_showcase_displayed'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='showcase_displayed',
            field=models.BooleanField(default=True, verbose_name='showcase_displayed'),
        ),
    ]
