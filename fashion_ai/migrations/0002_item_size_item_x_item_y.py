# Generated by Django 4.2.6 on 2024-01-06 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion_ai', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='x',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='y',
            field=models.IntegerField(default=0),
        ),
    ]
