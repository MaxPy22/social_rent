from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('special_equipment/', include('special_equipment.urls')),
]
