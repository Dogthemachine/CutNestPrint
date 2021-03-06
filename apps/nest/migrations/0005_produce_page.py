# Generated by Django 3.1.5 on 2021-07-21 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0004_auto_20210720_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produce_page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nest.items')),
                ('sizes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nest.sizes')),
            ],
            options={
                'verbose_name': 'produce',
                'verbose_name_plural': 'produce',
            },
        ),
    ]
