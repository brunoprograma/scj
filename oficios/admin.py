import logging
from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from rangefilter.filter import DateRangeFilter
from ajax_select.admin import AjaxSelectAdminStackedInline
from django.conf import settings
from django.contrib import admin, messages
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from agenda.admin import MyModelAdmin
from .models import *
from .forms import *
from .render import oficio_html_to_pdf

log = logging.getLogger('oficios.admin')


@admin.register(Cargo)
class CargoAdmin(MyModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome', )
    form = FormCargo


class ContatoEntidadeAdmin_Inline(AjaxSelectAdminStackedInline):
    list_display = ('telefone', 'celular', 'email')
    form = FormContatoEntidade
    model = ContatoEntidade


@admin.register(Entidade)
class EntidadeAdmin(MyModelAdmin):
    list_display = ('nome', 'regional', 'cargo', 'cidade')
    form = FormEntidade
    inlines = [ContatoEntidadeAdmin_Inline]
    search_fields = ('nome',)


@admin.register(Oficio)
class OficioAdmin(MyModelAdmin):
    list_display = ('id', 'data', 'regional', 'assunto')
    form = FormOficio
    search_fields = ('id', 'assunto')
    list_filter = (('data', DateRangeFilter),)
    actions = ['cadastrar_envio', 'print_oficio', 'email_oficio']

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

    def email_oficio(self, request, queryset):
        if len(queryset) == 1:
            mensagens = []
            connection = get_connection(
                username=None,
                password=None,
                fail_silently=False,
            )

            oficio = queryset[0]
            regional = oficio.regional
            endereco = oficio.deputado.endereco_principal

            form = None

            if 'send' in request.POST:
                if oficio and regional and endereco:
                    form = FormEscolheEntidade(request.POST, oficio=oficio)

                    if form.is_valid():
                        entidades = form.cleaned_data['entidades']

                        for entidade in entidades:
                            emails_destino = list(set(entidade.contatoentidade_set.all().values_list('email', flat=True)))

                            if emails_destino:
                                ctx = {
                                    'oficio': oficio,
                                    'regional': regional,
                                    'entidade': entidade,
                                    'endereco': oficio.deputado.endereco_principal
                                }

                                assunto_email = 'Ofício nº {} Deputado {}'.format(oficio, oficio.deputado)
                                corpo_email = render_to_string('email.html', ctx)
                                anexo = oficio_html_to_pdf('oficio.html', ctx)

                                mensagem = EmailMessage(assunto_email, corpo_email, endereco.email, emails_destino)
                                if anexo:
                                    mensagem.attach('Oficio_n{}.pdf'.format(oficio.id), anexo, 'application/pdf')
                                mensagens.append(mensagem)

                            else:
                                log.error('Entidade {} não possui e-mail para contato.', entidade)

                        try:
                            connection.send_messages(mensagens)
                        except Exception as e:
                            log.exception('Erro ao enviar e-mails do ofício {}: {}', oficio, e)
                            self.message_user(request, 'Erro ao enviar e-mails do ofício {}: {}'.format(oficio, e), level=messages.ERROR)
                        else:
                            self.message_user(request, 'Ofício enviado com sucesso.', level=messages.SUCCESS)
                        return HttpResponseRedirect(request.get_full_path())
                    else:
                        log.error('Dados insuficientes para enviar o Ofício {}. Precisamos do contato principal do Deputado {}', oficio, oficio.deputado)

            if not form:
                form = FormEscolheEntidade(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)}, oficio=oficio)

            context = {
                'oficios': queryset,
                'entidades_form': form,
                'site_header': settings.ADMIN_SITE_HEADER,
                'site_title': settings.ADMIN_SITE_TITLE,
                'index_title': settings.ADMIN_INDEX_TITLE
            }
            return render(request, 'admin/email_oficio.html', context)
        else:
            self.message_user(request, "Selecione apenas 1 Ofício para enviar.", level=messages.ERROR)
        return HttpResponseRedirect(request.get_full_path())

    email_oficio.short_description = "Enviar Ofício selecionado por e-mail"
