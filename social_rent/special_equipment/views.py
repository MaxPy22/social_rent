from django.shortcuts import render 
from .models import Category, Type, EquipmentModel, EquipmentUnit


def index(request):
    num_units = EquipmentUnit.objects.all().count()
    num_units_available = EquipmentUnit.objects.filter(status__exact='ok').count()

    context = {
        'num_units': num_units,
        'num_units_available': num_units_available,
    }

    return render(request, 'special_equipment/index.html', context)
