# Generated by Django 2.1.7 on 2019-05-28 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PumpManager', '0009_auto_20190522_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='adress',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='game',
            field=models.ManyToManyField(blank=True, null=True, to='PumpManager.Mix'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
