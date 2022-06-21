from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('special_equipment/<int:equipmentmodel_id>/', views.equipmentmodel, name='equipmentmodel'),
]