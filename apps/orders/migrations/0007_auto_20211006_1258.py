# Generated by Django 3.1.5 on 2021-10-06 09:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_globalsettings_this_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='jpeg_path',
            field=models.CharField(default=django.utils.timezone.now, max_length=256, verbose_name='tif_path'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='image_preview',
            field=models.FileField(blank=True, upload_to='photos_orders/'),
        ),
    ]