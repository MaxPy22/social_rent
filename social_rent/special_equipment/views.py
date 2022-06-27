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
from .forms import EquipmentModelReviewForm

@csrf_protect
def register(request):
    if request.method == "POST":
        # duomenu surinkimas
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # validuosim forma, tikrindami ar sutampa slaptažodžiai, ar egzistuoja vartotojas
        error = False
        if not password or password != password2:
            messages.error(request, 'Slaptažodžiai nesutampa arba neįvesti.')
            error = True
        if not username or User.objects.filter(username=username).exists():
            messages.error(request, f'Vartotojas {username} jau egzistuoja arba neįvestas.')
            error = True
        if not email or User.objects.filter(email=email).exists():
            messages.error(request, f'Vartotojas su el.praštu {email} jau egzistuoja arba neįvestas.')
            error = True
        if error:
            return redirect('register')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'Vartotojas {username} užregistruotas sėkmingai. Galite prisijungti')
            return redirect('index')
    return render(request, 'special_equipment/register.html')

def index(request):
    num_units = EquipmentUnit.objects.all().count()
    num_units_available = EquipmentUnit.objects.filter(status__exact='ok').count()
    
    context = {
        'num_units': num_units,
        'num_units_available': num_units_available,
    }

    return render(request, 'special_equipment/index.html', context)


def types(request):
    paginator = Paginator(Type.objects.all(), 4)
    page_number = request.GET.get('page')
    types = paginator.get_page(page_number)
    return render(request, 'special_equipment/types.html', {'types': types})

def type(request, type_id): ## equipmentmodel.html - nepabaigta
    type = get_object_or_404(Type, pk=type_id)
    return render(request, 'special_equipment/type.html', {'type': type})


# # 
# def equipmentmodel(request, equipmentmodel_id): ## equipmentmodel.html - nepabaigta
#     equipmentmodel = get_object_or_404(EquipmentModel, pk=equipmentmodel_id)
#     return render(request, 'special_equipment/equipmentmodel.html', {'equipmentmodel': equipmentmodel})

# def equipmentmodels(request):
#     paginator = Paginator(EquipmentModel.objects.all(), 5)
#     page_number = request.GET.get('page')
#     equipmentmodels = paginator.get_page(page_number)
#     return render(request, 'special_equipment/equipmentmodels.html', {'equipmentmodels': equipmentmodels})
##


class EquipmentModelsListView(generic.ListView):
    model = EquipmentModel
    context_object_name = 'equipment_models_list' # pagal nutylejima butu equipmentmodel_list
    template_name = 'special_equipment/equipmentmodels_list.html'
    extra_context = {'spalva': '#fc0'}
    paginate_by = 10

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
        context.update({'spalva': 'wheat'})
        return context


class EquipmentModelDetailView(generic.DetailView, FormMixin):
    model = EquipmentModel
    template_name = 'special_equipment/equipmentmodel_details.html'
    form_class = EquipmentModelReviewForm

    def get_success_url(self):
        return reverse('equipmentmodelurl', kwargs={'pk': self.object.id })
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.equipment_model = self.object
        form.instance.commentator = self.request.user
        form.save()
        return super().form_valid(form)
##

class LoanedEquipmentByPation(LoginRequiredMixin, generic.ListView):
    model = EquipmentUnit
    context_object_name = 'equipment_unit_list' # pagal nutylejima butu equipmentunit_list
    template_name = 'special_equipment/user_equipmentmodel_list.html'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(patient=self.request.user).filter(Q(status__exact='p') | Q(status__exact='r')).order_by('returning_date')

