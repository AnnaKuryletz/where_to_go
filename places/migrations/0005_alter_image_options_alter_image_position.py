# Generated by Django 5.2 on 2025-04-13 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_alter_place_detailsurl'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['position']},
        ),
        migrations.AlterField(
            model_name='image',
            name='position',
            field=models.SmallIntegerField(db_index=True, default=0, verbose_name='Позиция'),
        ),
    ]
