# Generated by Django 3.1.5 on 2021-10-02 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_clothesinorders_globalsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='result_tif_path',
            field=models.CharField(default='', max_length=256, verbose_name='tif_path'),
            preserve_default=False,
        ),
    ]