from django.contrib import admin
from .models import *
from .forms import *


class UsuarioAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'deputado')
    list_filter = ('deputado',)


class EnderecoDeputadoAdmin(admin.StackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormEnderecoDeputado
    model = EnderecoDeputado


class DeputadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'partido', 'estado')  #Deputado.objects.filter()
    list_filter = ('partido', 'estado')
    search_fields = ('nome', )
    inlines = [EnderecoDeputadoAdmin, ]


class PaisAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla')
    search_fields = ('nome', 'sigla')


class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    search_fields = ('nome',)


class RegionalAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    search_fields = ('nome',)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Deputado, DeputadoAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Estado, EstadoAdmin)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Partido, PaisAdmin)
admin.site.register(Regional, RegionalAdmin)
