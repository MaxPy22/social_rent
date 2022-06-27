from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('equipmentmodel', views.equipmentmodel, name='equipmentmodel'),
    path('type/<int:type_id>/', views.type, name='typeurl'),

    # path('equipmentmodels/<int:equipmentmodel_id>/', views.equipmentmodels, name='equipmentmodels'),
    path('types/', views.types , name='typesurl'),

    path('equipmentmodels/', views.EquipmentModelsListView.as_view() , name='equipmentmodelsurl'),
    
    # path('equipmentmodeldetails/', views.EquipmentModelDetailView.as_view() , name='modeldetails'),
    path('equipmentmodel/<int:pk>/', views.EquipmentModelDetailView.as_view(), name='equipmentmodelurl'),

    path('my_equpments/', views.LoanedEquipmentByPation.as_view(), name='my_equpmentsurl'),

    path('register/', views.register, name='register'),
]