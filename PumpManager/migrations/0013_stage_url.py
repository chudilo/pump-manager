# Generated by Django 2.1.7 on 2019-05-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PumpManager', '0012_auto_20190529_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='url',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
