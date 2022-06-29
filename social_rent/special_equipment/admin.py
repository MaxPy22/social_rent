from django.contrib import admin
from .models import Category, Type, EquipmentModel, EquipmentUnit, EquipmentModelComment


class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_title', 'get_models_count', )
    list_display_links = ('type_title', )
    search_fields = ('type_title', )


class EquipmentUnitInline(admin.TabularInline):
    model = EquipmentUnit
    can_delete = False
    extra = 0


class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_name', 'description', 'type', 'show_categories', )
    list_filter = ('type', 'category', )
    inlines = (EquipmentUnitInline, )


class EquipmentUnitAdmin(admin.ModelAdmin):
    list_display = ('equipment_model', 'id', 'status', 'returning_date', 'after_returning_date', 'notes', 'patient', )
    list_filter = ('status','returning_date', )
    search_fields = ('equipment_model__model_name', 'patient__username', )
    readonly_fields = ('id', )
    list_editable = ('status', 'returning_date', 'patient', )

    fieldsets = (
        ('Pagrindinė Informacija', {'fields': (
                'equipment_model',
                ('status', 'returning_date', )
            )}),
        ('Kita informacija', {'fields': (
                ('patient', 'notes', )
            )}),
)


class EquipmentModelCommentAdmin(admin.ModelAdmin):
    list_display = ('commentator', 'content', 'id', 'created_at', )
    list_filter = ('commentator','created_at', )
    search_fields = ('commentator', 'content', )


admin.site.register(Category)
admin.site.register(Type, TypeAdmin)
admin.site.register(EquipmentModel, EquipmentModelAdmin)
admin.site.register(EquipmentUnit, EquipmentUnitAdmin)
admin.site.register(EquipmentModelComment, EquipmentModelCommentAdmin)
