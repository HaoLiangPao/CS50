# Generated by Django 3.1.6 on 2021-03-24 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210323_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='bids',
            new_name='watchList',
        ),
        migrations.RemoveField(
            model_name='user',
            name='comments',
        ),
    ]
