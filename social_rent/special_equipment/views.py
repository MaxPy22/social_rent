from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Category, Type, EquipmentModel, EquipmentUnit
from django.db.models import Q
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect

# from .forms import ModelReviewForm

def index(request):
    num_units = EquipmentUnit.objects.all().count()
    num_units_available = EquipmentUnit.objects.filter(status__exact='ok').count()


    context = {

        'num_units_available': num_units_available,


    return render(request, 'special_equipment/index.html', context)

def type(request, type_id): ## equipmentmodel.html - nepabaigta
    type = get_object_or_404(EquipmentModel, pk=type_id)
    return render(request, 'special_equipment/type.html', {'type': type})

def types(request):
    paginator = Paginator(Type.objects.all(), 5)
    page_number = request.GET.get('page')
    types = paginator.get_page(page_number)
    return render(request, 'special_equipment/types.html', {'types': types})

# # 


class EquipmentModelsListView(generic.ListView):
    model = EquipmentModel
    context_object_name = 'equipment_models_list' # pagal nutylejima butu equipmentmodel_list
    template_name = 'special_equipment/equipmentmodels_list.html'
    extra_context = {'spalva': '#fc0'}
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            queryset = queryset.filter(
                Q(model_name__icontains=search) |
                Q(summary__icontains=search) |
                Q(type__type_title__istartswith=search)
            )
        return queryset

    def get_context_data(self, **kwargs): ## equipmentmodels_list 20 eilute - nebereikia
        context = super().get_context_data(**kwargs)
        context.update({'spalva': 'wheat'}) #overwrites self.extra_context if matched as well
        return context


class EquipmentModelDetailView(generic.DetailView, FormMixin):
    model = EquipmentModel
    template_name = 'special_equipment/equipmentmodels_details.html'
    # form_class = EquipmentModelReviewForm

    def get_success_url(self):
        return reverse('equipmentmodel', kwargs={'pk': self.object.id })
    