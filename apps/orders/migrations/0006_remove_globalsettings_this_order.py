# Generated by Django 3.1.5 on 2021-10-02 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_globalsettings_result_tif_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='globalsettings',
            name='this_order',
        ),
    ]
