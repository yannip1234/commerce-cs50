# Generated by Django 3.1.4 on 2021-01-03 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_bid', models.FloatField()),
                ('user_bid', models.FloatField()),
                ('user_id', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='listings',
            name='category',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]