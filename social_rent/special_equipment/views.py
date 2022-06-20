from django.shortcuts import render, get_object_or_404, reverse
from .models import Category, Type, EquipmentModel, EquipmentUnit


def index(request):
    num_units = EquipmentUnit.objects.all().count()
    num_units_available = EquipmentUnit.objects.filter(status__exact='ok').count()

    context = {

        'num_units': num_units,
        'num_units_available': num_units_available,

    }

    return render(request, 'special_equipment/index.html', context)


def EquipmentModel(request, equipmentmodel_id):
    equipmentmodel = get_object_or_404(EquipmentModel, pk=equipmentmodel_id)
    return render(request, 'special_equipment/equipmentmodel.html', {'equipmentmodel': equipmentmodel})
