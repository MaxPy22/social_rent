from django.db import models
import uuid
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from datetime import date

# from django.contrib.auth.models import User
# from django.utils.translation import gettext_lazy as _
# from datetime import date



# Create your models here.
class Category(models.Model): # priemoniu kategorijos
    category_title = models.CharField('Spec. priemonių kategorijos', max_length=156, help_text='nurodyti kateogoriją (pvz. judėjimo, higienos reikmenys ir t.t.)')

    def __str__(self):
        return self.category_title

    class Meta:
        ordering = ['category_title']
        verbose_name = 'Spec. priemonės kategorija'
        verbose_name_plural = 'spec. priemonių kategorijos'


class Type(models.Model): # priemoniu rusys, tipai
    type_title = models.CharField(('rūšis'), max_length=156, help_text='nurodyti konkrečią rūšį (pvz. neigaliojo vežimėlis, funkcinė lova ir pan.)')
    description = models.CharField('trumpas aprašymas', max_length=156, help_text='keli rūšies pavyzdžiai ir kita svarbiausia informacija', default="-")
    category = models.ManyToManyField(Category, verbose_name='Kategorija', related_name='types', help_text='nurodykit priemonės kategoriją')

    def __str__(self):
        return self.type_title

        
    def get_models_count(self):
        return self.equipment_models.count()
    get_models_count.short_description = 'bendras skirtingų modelių kiekis'

    class Meta:
        ordering = ['type_title']
        verbose_name = 'spec.priemonės rūšis'
        verbose_name_plural = 'spec.priemonių rūšys'


class EquipmentModel(models.Model): # turimu priemoniu konkretus modeliai
    model_name = models.CharField('gaminio modelio pavadinimas', max_length=156)
    # description = models.TextField('trumpas aprašymas/pagrindinės modelio savybės', max_length=1000, default='informacija tikslinama')
    description = HTMLField('arašymas,pagrindinės modelio savybės', help_text='svarbiausia informacija apie gaminį', default='informacija tikslinama')
    # image = models.ImageField(_('gaminio foto'), upload_to='apps/images', null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, related_name='equipment_models', verbose_name='priemonės rūšis')
    category = models.ManyToManyField(Category, related_name='equipment_models', verbose_name='Kategorija', help_text='nurodykit priemonės kategoriją')

    def __str__(self):
        return f'{str(self.type)} - {self.model_name}'

    class Meta:
        ordering = ['model_name']
        verbose_name = 'spec. priemonės modelis'
        verbose_name_plural = 'spec. priemonių modeliai'

    def show_categories(self):
        return ', '.join(category.category_title for category in self.category.all()[:5])
    show_categories.short_description = ('kategorijos')

    def get_available_units(self):
        return self.equipment_units.filter(status__exact='ok').count()
    get_available_units.short_description = ('laisvų priemonių kiekis')


class EquipmentUnit(models.Model): # turimu priemoniu apskaitiniai vienetai
    # inventory_number = models.UUIDField('inventorinis numeris', primary_key=True, default=uuid.uuid4, help_text='apskaitomam priemonės vienetui suteiktas unikalus inventorinis numeris', editable=False)
    id = models.UUIDField('inventorinis numeris', primary_key=True, default=uuid.uuid4, help_text='apskaitomam priemonės vienetui suteiktas unikalus inventorinis numeris', editable=False)
    notes = models.CharField(('pastabos'), max_length=224, null=True, default='-')
    returning_date = models.DateField('perduota iki: ', null=True, blank=True, db_index=True)
    equipment_model = models.ForeignKey(EquipmentModel, on_delete=models.PROTECT, null=True, related_name='equipment_units', verbose_name='spec. priemonė')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, related_name='equipment_units', verbose_name='kategorija')    
    patient = models.ForeignKey(User, on_delete=models.PROTECT, related_name= 'equipment_units', verbose_name=('pacientas'), null=True, blank=True, )
    
    AVAILABILITY = (
        ('ok', 'sandėlyje/prieinama'),
        ('p', 'paimta'),
        ('r', 'reservuota'),
        ('s', 'sugadinta (reikalingas remontas)'),
        ('no', 'naudojimui netinkama(nurašytina)'),
        ('kt', 'kitas statusas (priemonė neprieinama)'),
    )

    status = models.CharField('prieinamumas', max_length=2, choices=AVAILABILITY, blank=True, default='ok', db_index=True)
    
    def __str__(self):
        return f'{str(self.equipment_model.model_name)} - {str(self.id)}'


    class Meta:
        # ordering = ['returning_date']
        verbose_name = 'spec. priemonės vienetas'
        verbose_name_plural = 'spec. priemonių atsargos'

class EquipmentModelComment(models.Model):
    equipment_model = models.ForeignKey(
        EquipmentModel, 
        on_delete=models.CASCADE, 
        related_name='equipment_model_comments', 
        verbose_name='modelis',
        null=True, blank=True,
    )
    commentator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='model_comments',
        verbose_name='commentator',
        null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = HTMLField('atsiliepimas')

    def __str__(self):
        return f'{self.equipment_model} - {self.commentator} - {self.created_at}'


    class Meta:
        ordering = ['created_at']
        verbose_name = 'vartotojo komentaras'
        verbose_name_plural = 'vartotojų komentarai'
