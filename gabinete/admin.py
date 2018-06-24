from django.contrib import admin
from django.contrib.auth.admin import User, UserAdmin
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
    form = FormUsuario


class EnderecoDeputado_Inline(admin.StackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormEnderecoDeputado
    model = EnderecoDeputado


@admin.register(Deputado)
class DeputadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'partido', 'estado')
    list_filter = ('partido', 'estado')
    search_fields = ('nome', )
    inlines = [EnderecoDeputado_Inline]

    def is_customer(self, user):
        usuario = getattr(user, 'usuario', None)
        return (not user.is_superuser) and usuario

    def get_queryset(self, request):
        queryset = super(DeputadoAdmin, self).get_queryset(request)
        if self.is_customer(request.user):
            return queryset.filter(deputado=request.user.usuario.deputado)
        return queryset

    def has_change_permission(self, request, obj=None):
        permission = super(DeputadoAdmin, self).has_change_permission(request=request, obj=obj)
        obj_deputado = obj

        if obj_deputado and self.is_customer(request.user) and request.user.usuario.deputado != obj_deputado:
            return False

        return permission

    def has_delete_permission(self, request, obj=None):
        permission = super(DeputadoAdmin, self).has_delete_permission(request=request, obj=obj)
        obj_deputado = obj

        if obj_deputado and self.is_customer(request.user) and request.user.usuario.deputado != obj_deputado:
            return False

        return permission


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
class RegionalAdmin(MyModelAdmin):
    list_display = ('nome', )
    search_fields = ('nome',)
    form = FormRegional


admin.site.unregister(User)


@admin.register(User)
class MyUserAdmin(UserAdmin):

    def is_customer(self, user):
        usuario = getattr(user, 'usuario', None)
        return (not user.is_superuser) and usuario

    def has_change_permission(self, request, obj=None):
        perm = super(MyUserAdmin, self).has_change_permission(request, obj)
        if obj and self.is_customer(request.user):
            return False

        return perm
