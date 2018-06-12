from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter
from .models import *
from .forms import *


class TipoCompromissoAdmin(admin.ModelAdmin):
    list_display = ('deputado', 'nome')
    search_fields = ('nome',)


class CompromissoAdmin(admin.ModelAdmin):
    list_display = ('deputado', 'cidade', 'local', 'data_hora_inicio', 'data_hora_fim', 'tipo')
    form = FormCompromisso
    search_fields = ('deputado', 'local')
    list_filter = (('data_hora_inicio', DateTimeRangeFilter),)


class CompanhiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_filter = ('nome',)


class VooAdmin(admin.ModelAdmin):
    list_display = ('deputado', 'localizador', 'cidade_partida', 'data_hora_partida', 'cidade_chegada', 'data_hora_chegada')
    form = FormVoo
    search_fields = ('deputado','localizador')
    list_filter = (('data_hora_partida', DateTimeRangeFilter),)


admin.site.register(TipoCompromisso, TipoCompromissoAdmin)
admin.site.register(Compromisso, CompromissoAdmin)
admin.site.register(Companhia, CompanhiaAdmin)
admin.site.register(Voo, VooAdmin)