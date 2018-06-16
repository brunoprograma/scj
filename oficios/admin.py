from rangefilter.filter import DateRangeFilter
from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin
from django.db import transaction
from agenda.admin import MyModelAdmin
from .models import *
from .forms import *


@admin.register(Cargo)
class CargoAdmin(MyModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome', )
    form = FormCargo


class ContatoEntidadeAdmin_Inline(admin.StackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormContatoEntidade
    model = ContatoEntidade


@admin.register(Entidade)
class EntidadeAdmin(MyModelAdmin, AjaxSelectAdmin):
    list_display = ('nome', 'regional', 'cargo', 'cidade')
    form = FormEntidade
    inlines = [ContatoEntidadeAdmin_Inline]
    search_fields = ('nome',)


class EnvioOficioAdmin_Inline(admin.StackedInline):
    model = EnvioOficio
    readonly_fields = ('enviado', 'erros', 'data_hora_envio')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        perm = super(EnvioOficioAdmin_Inline, self).has_delete_permission(request, obj)
        if obj and not obj.enviado:
            return perm
        return False


@admin.register(Oficio)
class OficioAdmin(MyModelAdmin):
    list_display = ('id', 'data', 'regional', 'assunto')
    form = FormOficio
    search_fields = ('id', 'assunto')
    list_filter = (('data', DateRangeFilter),)
    inlines = [EnvioOficioAdmin_Inline]
    actions = ['cadastrar_envio']

    @transaction.atomic
    def cadastrar_envio(self, request, queryset):
        oficios = len(queryset)

        for oficio in queryset:
            if not oficio.enviooficio_set.filter(enviado=False).exists():
                EnvioOficio.objects.create(oficio=oficio)

        if oficios == 1:
            mensagem = "1 Ofício foi marcado"
        else:
            mensagem = "%s Ofícios foram marcados" % oficios
        self.message_user(request, "%s para envio." % mensagem)
    cadastrar_envio.short_description = "Enviar Ofícios selecionados"
