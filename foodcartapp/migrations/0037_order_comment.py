# Generated by Django 3.0.3 on 2020-10-02 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0036_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(default='', verbose_name='Комментарий'),
        ),
    ]
