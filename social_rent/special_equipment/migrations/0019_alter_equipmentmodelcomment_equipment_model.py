# Generated by Django 4.0.3 on 2022-06-27 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('special_equipment', '0018_alter_equipmentmodelcomment_commentator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentmodelcomment',
            name='equipment_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model_comments', to='special_equipment.equipmentmodel', verbose_name='modelis'),
        ),
    ]
