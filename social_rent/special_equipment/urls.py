from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('type/<int:type_id>/', views.type, name='type'),
    path('types/', views.types , name='types'),
    path('equipmentmodels/', views.EquipmentModelsListView.as_view() , name='equipmentmodels'),
    path('equipmentmodel/<int:pk>/', views.EquipmentModelDetailView.as_view(), name='equipmentmodel'),
    path('register/', views.register, name='register'),
    path('my_equipments/', views.LoanedEquipmentByPation.as_view(), name='my_equipments'),
    path('my_equipment/<uuid:pk>/', views.UnitsByUserDetailView.as_view(), name='my_equipment'),
    path('my_equipment/reservation/', views.reservation_info, name='reservation'),
    path('my_equipment/cancellation/<uuid:pk>/', views.UnitsByUserDeleteView.as_view(), name='cancel_my_reservation'),
]