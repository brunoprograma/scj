from itertools import chain
from operator import attrgetter
from datetime import datetime
from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin
from django.shortcuts import render
from django.utils import formats
from rangefilter.filter import DateTimeRangeFilter
from .models import *
from .forms import *


class MyModelAdmin(admin.ModelAdmin):
    def is_customer(self, user):
        return not user.is_superuser

    def get_queryset(self, request):
        queryset = super(MyModelAdmin, self).get_queryset(request)
        if self.is_customer(request.user):
            return queryset.filter(deputado=request.user.deputado)
        return queryset

    def has_change_permission(self, request, obj=None):
        permission = super(MyModelAdmin, self).has_change_permission(request=request, obj=obj)
        obj_deputado = getattr(obj, 'deputado', None)

        if obj_deputado and self.is_customer(request.user) and request.user.deputado != obj_deputado:
            return False

        return permission

    def has_delete_permission(self, request, obj=None):
        permission = super(MyModelAdmin, self).has_delete_permission(request=request, obj=obj)
        obj_deputado = getattr(obj, 'deputado', None)

        if obj_deputado and self.is_customer(request.user) and request.user.deputado != obj_deputado:
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
class TipoCompromissoAdmin(MyModelAdmin, AjaxSelectAdmin):
    list_display = ('deputado', 'nome')
    search_fields = ('nome',)
    form = FormTipoCompromisso


@admin.register(Compromisso)
class CompromissoAdmin(MyModelAdmin, AjaxSelectAdmin):
    list_display = ('deputado', 'cidade', 'local', 'data_hora_inicio', 'data_hora_fim', 'tipo')
    search_fields = ('deputado', 'local')
    list_filter = (('data_hora_inicio', DateTimeRangeFilter),)
    form = FormCompromisso
    change_list_template = 'admin/custom_change_list.html'

    def changelist_view(self, request, extra_context=None):
        mutable = request.GET._mutable
        request.GET._mutable = True
        print_roteiro = request.GET.pop('print', None)
        request.GET._mutable = mutable
        data_ini_gte_data = request.GET.get('data_hora_inicio__gte_0', None)
        data_ini_gte_hora = request.GET.get('data_hora_inicio__gte_1', None)
        data_ini_lte_data = request.GET.get('data_hora_inicio__lte_0', None)
        data_ini_lte_hora = request.GET.get('data_hora_inicio__lte_1', None)

        if print_roteiro and self.is_customer(request.user) and data_ini_gte_data and data_ini_gte_hora and \
                data_ini_lte_data and data_ini_lte_hora:
            deputado = request.user.deputado
            data_ini_gte_data = datetime.strptime(data_ini_gte_data, formats.get_format('DATE_INPUT_FORMATS')[0]).date()
            data_ini_gte_hora = datetime.strptime(data_ini_gte_hora, formats.get_format('TIME_INPUT_FORMATS')[0]).time()
            data_ini_lte_data = datetime.strptime(data_ini_lte_data, formats.get_format('DATE_INPUT_FORMATS')[0]).date()
            data_ini_lte_hora = datetime.strptime(data_ini_lte_hora, formats.get_format('TIME_INPUT_FORMATS')[0]).time()

            data_ini = datetime.combine(data_ini_gte_data, data_ini_gte_hora)
            data_fim = datetime.combine(data_ini_lte_data, data_ini_lte_hora)

            compromissos = Compromisso.objects.filter(deputado=deputado,
                                                      data_hora_inicio__range=[data_ini,
                                                                               data_fim])
            voos = Voo.objects.filter(deputado=deputado, data_hora_partida__range=[data_ini,
                                                                                   data_fim])

            itens = sorted(chain(compromissos, voos), key=attrgetter('data_hora'))

            ctx = {
                'deputado': deputado,
                'inicio': data_ini,
                'fim': data_fim,
                'itens': itens
            }

            return render(request, 'email.html', ctx)

        return super(CompromissoAdmin, self).changelist_view(request, extra_context)


@admin.register(Companhia)
class CompanhiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_filter = ('nome',)


@admin.register(Voo)
class VooAdmin(MyModelAdmin, AjaxSelectAdmin):
    list_display = ('deputado', 'localizador', 'cidade_partida', 'data_hora_partida', 'cidade_chegada', 'data_hora_chegada')
    search_fields = ('deputado','localizador')
    list_filter = (('data_hora_partida', DateTimeRangeFilter),)
    form = FormVoo
