# Generated by Django 2.2.1 on 2019-06-22 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='mask',
            new_name='is_label',
        ),
    ]
