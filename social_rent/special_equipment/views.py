from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Type, EquipmentModel, EquipmentUnit
from django.db.models import Q
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from .forms import EquipmentModelReviewForm
from django.urls import reverse, reverse_lazy


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
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

def type(request, type_id): 
    type = get_object_or_404(Type, pk=type_id)
    return render(request, 'special_equipment/type.html', {'type': type})

def reservation_info(request,): 
    return render(request, 'special_equipment/user_reservation_info.html', {'type': type})


class EquipmentModelsListView(generic.ListView):
    model = EquipmentModel
    context_object_name = 'equipment_models_list'
    template_name = 'special_equipment/equipmentmodels_list.html'
    extra_context = {'spalva': '#fc0'}
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('search_name'):
            search_text = self.request.GET.get('search_name')
            queryset = queryset.filter(
                Q(model_name__icontains=search_text) |
                Q(type__type_title__icontains=search_text)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'spalva': 'wheat'})
        return context


class EquipmentModelDetailView(generic.DetailView, FormMixin):
    model = EquipmentModel
    template_name = 'special_equipment/equipmentmodel_details.html'
    form_class = EquipmentModelReviewForm

    def get_success_url(self):
        return reverse('equipmentmodel', kwargs={'pk': self.object.id })
    
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


class LoanedEquipmentByPation(LoginRequiredMixin, generic.ListView):
    model = EquipmentUnit
    context_object_name = 'equipmentunit_list'
    template_name = 'special_equipment/user_equipment_list.html'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(patient=self.request.user).filter(Q(status__exact='p') | Q(status__exact='r')).order_by('returning_date')


class UnitsByUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = EquipmentUnit
    template_name = 'special_equipment/user_unit_detail.html'


class UnitsByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = EquipmentUnit
    success_url = reverse_lazy('my_equipments')
    template_name = 'special_equipment/user_unit_delete.html'

    def test_func(self):
        equipment_unit = self.get_object()
        return equipment_unit.patient == self.request.user