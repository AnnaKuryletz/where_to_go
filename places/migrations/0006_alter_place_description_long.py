# Generated by Django 5.2 on 2025-04-13 22:54

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_alter_image_options_alter_image_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='description_long',
            field=tinymce.models.HTMLField(verbose_name='Подробное описание'),
        ),
    ]
