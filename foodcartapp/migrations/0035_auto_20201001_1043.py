# Generated by Django 3.0.3 on 2020-10-01 07:43

from django.db import migrations


def fill_product_total(apps, schema_editor):
    OrderProduct = apps.get_model('foodcartapp', 'OrderProduct')
    for order_product in OrderProduct.objects.all():
        order_product.product_total = order_product.product.price * order_product.quantity
        order_product.save()


def empty_product_total(apps, schema_editor):
    OrderProduct = apps.get_model('foodcartapp', 'OrderProduct')
    for order_product in OrderProduct.objects.all():
        order_product.product_total = ''
        order_product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0034_orderproduct_product_total'),
    ]

    operations = [
        migrations.RunPython(fill_product_total, empty_product_total)
    ]