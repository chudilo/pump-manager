# Generated by Django 2.1.7 on 2019-05-08 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PumpManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(max_length=40, unique='True'),
        ),
    ]
