# Generated by Django 3.1.5 on 2021-09-05 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='material type')),
            ],
            options={
                'verbose_name': 'material type',
                'verbose_name_plural': 'material type',
            },
        ),
        migrations.CreateModel(
            name='Rolls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=5, verbose_name='material')),
                ('initially_meters', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='initially meters')),
                ('actual_meters', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='actual meters')),
                ('date_of_purchase', models.DateTimeField(verbose_name='date of manufacture')),
                ('material_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.materialtypes')),
            ],
            options={
                'verbose_name': 'orders',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_rates', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='coast rate')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
                ('amount_of_units', models.PositiveSmallIntegerField(default=0, verbose_name='amount of units')),
                ('amount_of_material', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='amount of material')),
                ('expected_cost', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='expected cost')),
                ('actual_cost', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='actual cost')),
                ('date_of_manufacture', models.DateTimeField(verbose_name='date of manufacture')),
                ('roll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.rolls')),
            ],
            options={
                'verbose_name': 'orders',
                'verbose_name_plural': 'orders',
                'ordering': ('added',),
            },
        ),
    ]