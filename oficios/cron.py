import logging
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from .models import EnvioOficio
from .render import oficio_html_to_pdf

log = logging.getLogger('oficios.cron')


def envia_oficios():
    mensagens = []
    connection = get_connection(
        username=None,
        password=None,
        fail_silently=False,
    )

    for envio in EnvioOficio.objects.filter(enviado=False):
        oficio = envio.oficio
        regional = oficio.regional
        endereco = oficio.deputado.endereco_principal

        if oficio and regional and endereco:
            for entidade in regional.entidade_set.ativos(deputado=oficio.deputado):
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
                if not envio.erros:
                    envio.erros = ''
                envio.erros += '{}\n'.format(e)
            else:
                envio.enviado = True
                envio.data_hora_envio = timezone.now()
            envio.save()
        else:
            log.error('Dados insuficientes para enviar o Ofício {}. Precisamos do contato principal do Deputado {}', oficio, oficio.deputado)
