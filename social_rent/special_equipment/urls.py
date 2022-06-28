from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('type/<int:type_id>/', views.type, name='typeurl'),
    path('types/', views.types , name='typesurl'),
    path('equipmentmodels/', views.EquipmentModelsListView.as_view() , name='equipmentmodelsurl'),
    path('equipmentmodel/<int:pk>/', views.EquipmentModelDetailView.as_view(), name='equipmentmodelurl'),
    path('my_equpments/', views.LoanedEquipmentByPation.as_view(), name='my_equpmentsurl'),
    path('register/', views.register, name='register'),
]