# Generated by Django 3.1.4 on 2021-01-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210103_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='starting_bid',
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(),
        ),
    ]
