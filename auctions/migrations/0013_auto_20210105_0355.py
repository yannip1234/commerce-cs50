# Generated by Django 3.1.4 on 2021-01-05 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20210105_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='user_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
