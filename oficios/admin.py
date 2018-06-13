from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import *
from .forms import *


class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome', )


class ContatoEntidadeAdmin(admin.StackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormContatoEntidade
    model = ContatoEntidade


class EntidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'regional', 'cargo', 'cidade')
    form = FormEntidade
    inlines = [ContatoEntidadeAdmin,]
    search_fields = ('nome',)


class OficioAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'regional', 'assunto')
    form = FormOficio
    search_fields = ('id', 'assunto')
    list_filter = (('data', DateRangeFilter),)


admin.site.register(Cargo, CargoAdmin)
admin.site.register(Entidade, EntidadeAdmin)
admin.site.register(Oficio, OficioAdmin)