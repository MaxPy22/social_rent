from django import forms
from django.conf import settings
from tinymce.widgets import TinyMCE
from .models import EquipmentModelComment


class EquipmentModelReviewForm(forms.ModelForm):
    class Meta:
        model = EquipmentModelComment
        fields = ('content', 'equipment_model', 'commentator', )
        widgets = {
            'content': TinyMCE(mce_attrs=settings.TINYMCE_USER_CONFIG),
            'equipment_model': forms.HiddenInput(),
            'commentator': forms.HiddenInput(),
        }
