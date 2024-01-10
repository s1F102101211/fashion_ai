# Generated by Django 4.2.6 on 2024-01-06 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fashion_ai', '0002_item_size_item_x_item_y'),
    ]

    operations = [
        migrations.RenameField(
            model_name='design',
            old_name='category1',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='design',
            old_name='img',
            new_name='path',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='category1',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='category2',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='img',
            new_name='path',
        ),
        migrations.RemoveField(
            model_name='design',
            name='category2',
        ),
        migrations.RemoveField(
            model_name='design',
            name='item_id',
        ),
    ]