# Generated by Django 3.1.6 on 2021-03-25 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210324_1457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='created',
            new_name='createdAt',
        ),
        migrations.AddField(
            model_name='auction',
            name='createdBy',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]