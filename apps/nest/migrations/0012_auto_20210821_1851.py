# Generated by Django 3.1.5 on 2021-08-21 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0011_categories_showcase_displayed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pieces',
            name='image',
            field=models.FileField(blank=True, upload_to='photos_pieces/'),
        ),
    ]
