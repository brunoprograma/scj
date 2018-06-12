from django.contrib import admin
from .models import *
from .forms import *


class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(MyModelAdmin, self).get_queryset(request)
        if not request.user.is_superuser and ('deputado' in self.model._meta.get_fields(include_hidden=True)):
            return queryset.filter(deputado=request.user.usuario.deputado)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'deputado')
    list_filter = ('deputado',)


@admin.register(Deputado)
class DeputadoAdmin(MyModelAdmin):
    list_display = ('nome', 'partido', 'estado')
    list_filter = ('partido', 'estado')
    search_fields = ('nome', )
    form = FormEnderecoDeputado


# admin.site.register(Usuario, UsuarioAdmin)
# admin.site.register(Deputado, DeputadoAdmin)
# admin.site.register(Pais)
# admin.site.register(Estado)
# admin.site.register(Cidade)
# admin.site.register(Partido)
# admin.site.register(Regional)
