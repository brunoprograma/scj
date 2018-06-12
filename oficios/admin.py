from django.contrib import admin
from .models import *
from .forms import FormEntidade, FormContatoEntidade, FormOficio


class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome',)


class ContatoEntidadeAdmin(admin.StackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormContatoEntidade
    model = ContatoEntidade


class EntidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'regional', 'cargo', 'cidade')
    form = FormEntidade
    inlines = [ContatoEntidadeAdmin,]


class OficioAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'regional', 'assunto')
    form = FormOficio


admin.site.register(Cargo, CargoAdmin)
admin.site.register(Entidade, EntidadeAdmin)
admin.site.register(Oficio, OficioAdmin)