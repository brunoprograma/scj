from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from rangefilter.filter import DateRangeFilter
from ajax_select.admin import AjaxSelectAdmin
from django.conf import settings
from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from agenda.admin import MyModelAdmin
from .models import *
from .forms import *
from .render import oficio_html_to_pdf


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


@admin.register(EnvioOficio)
class EnvioOficioAdmin(admin.ModelAdmin):
    model = EnvioOficio
    readonly_fields = ('enviado', 'erros', 'data_hora_envio')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        perm = super(EnvioOficioAdmin, self).has_delete_permission(request, obj)
        if obj and not obj.enviado:
            return perm
        return False


@admin.register(Oficio)
class OficioAdmin(MyModelAdmin):
    list_display = ('id', 'data', 'regional', 'assunto')
    form = FormOficio
    search_fields = ('id', 'assunto')
    list_filter = (('data', DateRangeFilter),)
    actions = ['cadastrar_envio', 'print_oficio']

    def print_oficio(self, request, queryset):
        if len(queryset) == 1:
            oficio = queryset[0]
            form = None
            if 'print' in request.POST:
                form = FormEscolheEntidade(request.POST, oficio=oficio)

                if form.is_valid():
                    response = HttpResponse(content_type="application/pdf")
                    output = PdfFileWriter()
                    success = True

                    entidades = form.cleaned_data['entidades']

                    for entidade in entidades:
                        params = {
                            'oficio': oficio,
                            'regional': oficio.regional,
                            'entidade': entidade,
                            'endereco': oficio.deputado.endereco_principal
                        }

                        pdf_response = oficio_html_to_pdf('oficio.html', params)

                        if not pdf_response:
                            success = False
                            break
                        else:
                            input = PdfFileReader(BytesIO(pdf_response))
                            pages = input.pages
                            for page in pages:
                                output.addPage(page)

                    if success:
                        outputStream = BytesIO()
                        output.write(outputStream)
                        response.write(outputStream.getvalue())
                        return response
                    else:
                        self.message_user(request, "Erro ao gerar PDF.", level=messages.ERROR)
                        return HttpResponseRedirect(request.get_full_path())

            if not form:
                form = FormEscolheEntidade(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)}, oficio=oficio)

            context = {
                'oficios': queryset,
                'entidades_form': form,
                'site_header': settings.ADMIN_SITE_HEADER,
                'site_title': settings.ADMIN_SITE_TITLE,
                'index_title': settings.ADMIN_INDEX_TITLE
            }
            return render(request, 'admin/print_oficio.html', context)

        self.message_user(request, "Selecione apenas 1 Ofício para imprimir.", level=messages.ERROR)
        return HttpResponseRedirect(request.get_full_path())

    print_oficio.short_description = "Imprimir Ofício selecionado"

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
