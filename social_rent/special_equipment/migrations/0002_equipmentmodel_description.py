# Generated by Django 4.0.3 on 2022-06-18 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('special_equipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentmodel',
            name='description',
            field=models.TextField(default='informacija tikslinama', max_length=1000, verbose_name='trumpas aprašymas/pagrindinės modelio savybės'),
        ),
    ]
