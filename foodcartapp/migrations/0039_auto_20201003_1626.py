# Generated by Django 3.0.3 on 2020-10-03 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20201003_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='registred_at',
            new_name='registrated_at',
        ),
    ]