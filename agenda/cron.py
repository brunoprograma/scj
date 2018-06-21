import logging
from itertools import chain
from operator import attrgetter
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from gabinete.models import Deputado, Usuario
from .models import Compromisso, Voo

log = logging.getLogger('agenda.cron')


def envia_agenda_semana():
    """
    Envia todos os domingos a agenda da semana para os Deputados ativos cadastrados no sistema
    e seus acessores cadastrados
    """
    segunda_data = timezone.now().date() + timedelta(1.0)
    segunda_data_hora = datetime(segunda_data.year,
                                 segunda_data.month,
                                 segunda_data.day, 0, 0, 0, 0)
    proxima_segunda = segunda_data + timedelta(7.0)
    proxima_segunda_data_hora = datetime(proxima_segunda.year,
                                         proxima_segunda.month,
                                         proxima_segunda.day, 0, 0, 0, 0) - timedelta(microseconds=1.0)

    mensagens = []

    for deputado in Deputado.objects.ativo():
        contato_deputado = deputado.endereco_principal

        if contato_deputado:
            compromissos = Compromisso.objects.filter(deputado=deputado,
                                                      data_hora_inicio__range=[segunda_data_hora,
                                                                               proxima_segunda_data_hora])
            voos = Voo.objects.filter(deputado=deputado, data_hora_partida__range=[segunda_data_hora,
                                                                                   proxima_segunda_data_hora])

            itens = sorted(chain(compromissos, voos), key=attrgetter('data_hora'))

            ctx = {
                'deputado': deputado,
                'inicio': segunda_data_hora,
                'fim': proxima_segunda_data_hora,
                'itens': itens
            }

            acessores = Usuario.objects.filter(deputado=deputado, ativo=True)

            assunto_email = 'Roteiro semanal do Deputado {}'.format(deputado)
            corpo_email = render_to_string('email.html', ctx)
            emails_destino = [contato_deputado.email]
            for acessor in acessores:
                if acessor.user.email:
                    emails_destino.append(acessor.user.email)

            mensagens.append((assunto_email, corpo_email, contato_deputado.email, emails_destino))
        else:
            log.error('Deputado {} não possui e-mail cadastrado.', deputado)

    if mensagens:
        try:
            send_mass_mail(mensagens)
        except Exception as e:
            log.exception('Erro ao enviar e-mails da agenda: {}', e)
