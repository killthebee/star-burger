# Generated by Django 3.0.3 on 2021-01-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_auto_20210127_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Адрес'),
        ),
    ]
