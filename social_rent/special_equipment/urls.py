from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('type/<int:type_id>/', views.type, name='typeurl'),
    path('types/', views.types , name='typesurl'),
    path('equipmentmodels/', views.EquipmentModelsListView.as_view() , name='equipmentmodelsurl'),
    path('equipmentmodel/<int:pk>/', views.EquipmentModelDetailView.as_view(), name='equipmentmodelurl'),
    path('register/', views.register, name='register'),
    path('my_equipments/', views.LoanedEquipmentByPation.as_view(), name='my_equipmentsurl'),
    path('my_equipment/<uuid:pk>/', views.UnitsByUserDetailView.as_view(), name='my_equipmenturl'),
    path('my_equipment/reservation/', views.UnitsByUserCreateView.as_view(), name='my_equipment_reservationurl'),
    path('my_equipment/cancellation/<uuid:pk>/', views.UnitsByUserDeleteView.as_view(), name='my_equipment_cancellationurl'),
]