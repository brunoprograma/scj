from django.contrib import admin
from .models import *
from .forms import *


class UsuarioAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'deputado')
    list_filter = ('deputado',)


class DeputadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'partido', 'estado')  #Deputado.objects.filter()
    list_filter = ('partido', 'estado')
    search_fields = ('nome', )
    form = FormEnderecoDeputado


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Deputado, DeputadoAdmin)
admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Partido)
admin.site.register(Regional)
