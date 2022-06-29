from django.contrib import admin
from .models import Category, Type, EquipmentModel, EquipmentUnit, EquipmentModelComment


class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_title', 'get_models_count', )
    list_display_links = ('type_title', )
    search_fields = ('type_title', ) #, 'category', )


class EquipmentUnitInline(admin.TabularInline):
    model = EquipmentUnit
    can_delete = False
    extra = 0


class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_name', 'description', 'type', 'show_categories', )
    list_filter = ('type', 'category', )
    inlines = (EquipmentUnitInline, )


class EquipmentUnitAdmin(admin.ModelAdmin):

    # def user_details(*args, **kwargs):
    #     user_info = self.request.user

    # def get_queryset(self):
    #     user_info = super().get_queryset().self.request.user.full_name

    

    list_display = ('equipment_model', 'id', 'status', 'returning_date', 'notes', 'patient', ) # 'get_name') # 'patient')
    list_filter = ('status','returning_date', )
    search_fields = ('equipment_model__model_name', 'patient__username' )
    readonly_fields = ('id', )
    list_editable = ('status', 'returning_date', 'patient', )  # leidzia redaguoti isrinktus laukus prie bendro elementu saraso

    fieldsets = (
        ('Pagrindinė Informacija', {'fields': (
                'equipment_model',
                ('status', 'returning_date', )
            )}),
        ('Kita informacija', {'fields': (
                ('patient', 'notes',)
            )}),
)

    # def get_name(self, obj): # funkciją gali vadint kaip nori, svarbu būtų self ir obj
    #     return obj.patient.first_name # čia turi nurodyti tikslų kelią iki paciento vardo

admin.site.register(Category)
admin.site.register(Type, TypeAdmin)
admin.site.register(EquipmentModel, EquipmentModelAdmin)
admin.site.register(EquipmentUnit, EquipmentUnitAdmin)
admin.site.register(EquipmentModelComment)
