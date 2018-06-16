from django.contrib import admin
from agenda.admin import MyModelAdmin
from .models import *
from .forms import *


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('sigla', 'nome')


@admin.register(Usuario)
class UsuarioAdmin(MyModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'deputado')
    list_filter = ('deputado',)


class EnderecoDeputado_Inline(admin.StackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormEnderecoDeputado
    model = EnderecoDeputado


@admin.register(Deputado)
class DeputadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'partido', 'estado')
    list_filter = ('partido', 'estado')
    search_fields = ('nome', )
    inlines = [EnderecoDeputado_Inline, ]


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla')
    search_fields = ('nome', 'sigla')


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    search_fields = ('nome',)


@admin.register(Regional)
class RegionalAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    search_fields = ('nome',)
