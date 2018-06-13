from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter
from .models import *
from .forms import *


class MyModelAdmin(admin.ModelAdmin):
    def is_customer(self, user):
        usuario = getattr(user, 'usuario', None)
        return (not user.is_superuser) and usuario

    def get_queryset(self, request):
        queryset = super(MyModelAdmin, self).get_queryset(request)
        if self.is_customer(request.user):
            return queryset.filter(deputado=request.user.usuario.deputado)
        return queryset

    def has_change_permission(self, request, obj=None):
        permission = super(MyModelAdmin, self).has_change_permission(request=request, obj=obj)
        obj_deputado = getattr(obj, 'deputado', None)

        if obj_deputado and self.is_customer(request.user) and request.user.usuario.deputado != obj_deputado:
            return False

        return permission

    def has_delete_permission(self, request, obj=None):
        permission = super(MyModelAdmin, self).has_delete_permission(request=request, obj=obj)
        obj_deputado = getattr(obj, 'deputado', None)

        if obj_deputado and self.is_customer(request.user) and request.user.usuario.deputado != obj_deputado:
            return False

        return permission

    def get_form(self, request, obj=None, **kwargs):
        adminform = super(MyModelAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(adminform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                kwargs['is_customer'] = self.is_customer(request.user)
                return adminform(*args, **kwargs)

        return AdminFormWithRequest


@admin.register(TipoCompromisso)
class TipoCompromissoAdmin(MyModelAdmin):
    list_display = ('deputado', 'nome')
    search_fields = ('nome',)
    form = FormTipoCompromisso


@admin.register(Compromisso)
class CompromissoAdmin(MyModelAdmin):
    list_display = ('deputado', 'cidade', 'local', 'data_hora_inicio', 'data_hora_fim', 'tipo')
    search_fields = ('deputado', 'local')
    list_filter = (('data_hora_inicio', DateTimeRangeFilter),)
    form = FormCompromisso


@admin.register(Companhia)
class CompanhiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_filter = ('nome',)


@admin.register(Voo)
class VooAdmin(MyModelAdmin):
    list_display = ('deputado', 'localizador', 'cidade_partida', 'data_hora_partida', 'cidade_chegada', 'data_hora_chegada')
    search_fields = ('deputado','localizador')
    list_filter = (('data_hora_partida', DateTimeRangeFilter),)
    form = FormVoo
