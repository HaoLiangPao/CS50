# Generated by Django 3.1.6 on 2021-03-26 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210326_1757'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_category',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='auction_category',
            old_name='listing_id',
            new_name='listing',
        ),
    ]
