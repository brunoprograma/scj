from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from agenda.admin import MyModelAdmin
from .models import *
from .forms import *


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('sigla', 'nome')


class EnderecoDeputado_Inline(admin.StackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormEnderecoDeputado
    model = EnderecoDeputado


@admin.register(Deputado)
class DeputadoAdmin(admin.ModelAdmin):
    form = FormDeputado
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
            return queryset.filter(deputado=request.user.deputado)
        return queryset

    def has_change_permission(self, request, obj=None):
        permission = super(DeputadoAdmin, self).has_change_permission(request=request, obj=obj)
        obj_deputado = obj

        if obj_deputado and self.is_customer(request.user) and request.user.deputado != obj_deputado:
            return False

        return permission

    def has_delete_permission(self, request, obj=None):
        permission = super(DeputadoAdmin, self).has_delete_permission(request=request, obj=obj)
        obj_deputado = obj

        if obj_deputado and self.is_customer(request.user) and request.user.deputado != obj_deputado:
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


@admin.register(User)
class UserAdmin(BaseUserAdmin, MyModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('deputado', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('deputado', 'email', 'password1', 'password2'),
        }),
    )
    customer_fieldsets = (
        (None, {'fields': ('deputado', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'groups')}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        elif not request.user.is_superuser:
            return self.customer_fieldsets
        return super().get_fieldsets(request, obj)

    def is_customer(self, user):
        return not user.is_superuser

    def has_change_permission(self, request, obj=None):
        perm = super(UserAdmin, self).has_change_permission(request, obj)
        if obj and self.is_customer(request.user):
            if (not obj.deputado) or (obj.deputado != request.user.deputado):
                return False

        return perm
