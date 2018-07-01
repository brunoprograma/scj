from itertools import chain
from operator import attrgetter
from datetime import datetime
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import autoselect_fields_check_can_add
from django.conf import settings
from django.contrib import admin, messages
from django.shortcuts import render, HttpResponseRedirect
from django.utils import formats, timezone
from rangefilter.filter import DateTimeRangeFilter
from .models import *
from .forms import *


class MyModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super(MyModelAdmin, self).get_queryset(request)
        if request.user.deputado:
            return queryset.filter(deputado=request.user.deputado)
        return queryset

    def has_change_permission(self, request, obj=None):
        permission = super(MyModelAdmin, self).has_change_permission(request=request, obj=obj)
        obj_deputado = getattr(obj, 'deputado', None)

        if obj_deputado and (not request.user.is_superuser) and request.user.deputado != obj_deputado:
            return False

        return permission

    def has_delete_permission(self, request, obj=None):
        permission = super(MyModelAdmin, self).has_delete_permission(request=request, obj=obj)
        obj_deputado = getattr(obj, 'deputado', None)

        if obj_deputado and (not request.user.is_superuser) and request.user.deputado != obj_deputado:
            return False

        return permission

    def get_form(self, request, obj=None, **kwargs):
        adminform = super(MyModelAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(adminform):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return adminform(*args, **kwargs)

        form = AdminFormWithRequest

        autoselect_fields_check_can_add(form, self.model, request.user)
        return form


@admin.register(TipoCompromisso)
class TipoCompromissoAdmin(MyModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    form = FormTipoCompromisso


@admin.register(Compromisso)
class CompromissoAdmin(MyModelAdmin):
    list_display = ('tipo', 'local', 'cidade', 'data_hora_inicio', 'data_hora_fim')
    search_fields = ('local', )
    list_filter = (('data_hora_inicio', DateTimeRangeFilter),)
    form = FormCompromisso
    change_list_template = 'admin/custom_change_list.html'

    def changelist_view(self, request, extra_context=None):
        print_roteiro = request.GET.get('print', None)

        if print_roteiro:
            data_ini_gte_data = request.GET.get('data_hora_inicio__gte_0', None)
            data_ini_gte_hora = request.GET.get('data_hora_inicio__gte_1', None)
            data_ini_lte_data = request.GET.get('data_hora_inicio__lte_0', None)
            data_ini_lte_hora = request.GET.get('data_hora_inicio__lte_1', None)

            if data_ini_gte_data and data_ini_gte_hora and data_ini_lte_data and data_ini_lte_hora and request.user.deputado:
                deputado = request.user.deputado
                data_ini_gte_data = datetime.strptime(data_ini_gte_data, formats.get_format('DATE_INPUT_FORMATS')[0]).date()
                data_ini_gte_hora = datetime.strptime(data_ini_gte_hora, formats.get_format('TIME_INPUT_FORMATS')[0]).time()
                data_ini_lte_data = datetime.strptime(data_ini_lte_data, formats.get_format('DATE_INPUT_FORMATS')[0]).date()
                data_ini_lte_hora = datetime.strptime(data_ini_lte_hora, formats.get_format('TIME_INPUT_FORMATS')[0]).time()

                data_ini = datetime.combine(data_ini_gte_data, data_ini_gte_hora)
                data_fim = datetime.combine(data_ini_lte_data, data_ini_lte_hora)
                data_ini = data_ini.replace(tzinfo=timezone.get_current_timezone())
                data_fim = data_fim.replace(tzinfo=timezone.get_current_timezone())

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
                    'itens': itens,
                    'site_header': settings.ADMIN_SITE_HEADER,
                    'site_title': settings.ADMIN_SITE_TITLE,
                    'index_title': settings.ADMIN_INDEX_TITLE
                }

                return render(request, 'roteiro.html', ctx)
            else:
                self.message_user(request, 'Utilize o filtro de Data e Hora antes de imprimir o roteiro.', level=messages.WARNING)
                return HttpResponseRedirect(request.path)

        return super(CompromissoAdmin, self).changelist_view(request, extra_context)


@admin.register(Companhia)
class CompanhiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Voo)
class VooAdmin(MyModelAdmin):
    list_display = ('companhia', 'localizador', 'cidade_partida', 'data_hora_partida', 'cidade_chegada', 'data_hora_chegada')
    search_fields = ('localizador', 'numero')
    list_filter = (('data_hora_partida', DateTimeRangeFilter),)
    form = FormVoo
