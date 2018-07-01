from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminStackedInline
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


class EnderecoDeputado_Inline(AjaxSelectAdminStackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormEnderecoDeputado
    model = EnderecoDeputado


@admin.register(Deputado)
class DeputadoAdmin(AjaxSelectAdmin):
    form = FormDeputado
    list_display = ('nome', 'partido', 'estado')
    list_filter = ('partido', 'estado')
    search_fields = ('nome', )
    inlines = [EnderecoDeputado_Inline]

    def get_queryset(self, request):
        queryset = super(DeputadoAdmin, self).get_queryset(request)
        if request.user.deputado:
            return queryset.filter(id=request.user.deputado_id)
        return queryset

    def has_change_permission(self, request, obj=None):
        permission = super(DeputadoAdmin, self).has_change_permission(request=request, obj=obj)
        obj_deputado = obj

        if obj_deputado and (not request.user.is_superuser) and request.user.deputado != obj_deputado:
            return False

        return permission

    def has_delete_permission(self, request, obj=None):
        permission = super(DeputadoAdmin, self).has_delete_permission(request=request, obj=obj)
        obj_deputado = obj

        if obj_deputado and (not request.user.is_superuser) and request.user.deputado != obj_deputado:
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
    list_display = ('nome',)
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
    customer2_fieldsets = (
        (None, {'fields': ('deputado', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )

    def get_fieldsets(self, request, obj=None):
        groups = request.user.groups.all().values_list('id', flat=True)
        if not obj:
            return self.add_fieldsets
        elif 2 in groups and not request.user.is_superuser:
            return self.customer_fieldsets
        elif 1 in groups and not request.user.is_superuser:
            return self.customer2_fieldsets
        return super().get_fieldsets(request, obj)

    def has_change_permission(self, request, obj=None):
        perm = super(UserAdmin, self).has_change_permission(request, obj)
        if (2 not in request.user.groups.all().values_list('id', flat=True)) and obj and obj != request.user:
            return False

        return perm
