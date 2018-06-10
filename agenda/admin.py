from django.contrib import admin
from .models import *
from .forms import FormCompromisso, FormVoo


class TipoCompromissoAdmin(admin.ModelAdmin):
    list_display = ('deputado', 'nome')


class CompromissoAdmin(admin.ModelAdmin):
    list_display = ('deputado', 'cidade', 'local', 'data_hora_inicio', 'data_hora_fim', 'tipo')
    form = FormCompromisso


class CompanhiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


class VooAdmin(admin.ModelAdmin):
    list_display = ('deputado', 'cidade_partida', 'data_hora_partida', 'cidade_chegada', 'data_hora_chegada')
    form = FormVoo


admin.site.register(TipoCompromisso, TipoCompromissoAdmin)
admin.site.register(Compromisso, CompromissoAdmin)
admin.site.register(Companhia, CompanhiaAdmin)
admin.site.register(Voo, VooAdmin)