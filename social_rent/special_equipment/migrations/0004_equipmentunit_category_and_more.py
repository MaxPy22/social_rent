# Generated by Django 4.0.3 on 2022-06-19 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('special_equipment', '0003_alter_equipmentunit_id_alter_equipmentunit_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentunit',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='equipment_units', to='special_equipment.category', verbose_name='kategorija'),
        ),
        migrations.AlterField(
            model_name='equipmentunit',
            name='equipment_model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='equipment_units', to='special_equipment.equipmentmodel', verbose_name='spec. priemonė'),
        ),
    ]