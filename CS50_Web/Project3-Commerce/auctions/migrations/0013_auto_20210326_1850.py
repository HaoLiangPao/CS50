# Generated by Django 3.1.6 on 2021-03-26 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20210326_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.IntegerField(),
        ),
    ]
