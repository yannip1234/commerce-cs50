# Generated by Django 3.1.4 on 2021-01-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210103_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img_url',
            field=models.URLField(blank=True),
        ),
    ]
