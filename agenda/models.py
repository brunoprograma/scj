from django.db import models
from gabinete.models import DeputadoManager


class TipoCompromisso(models.Model):
    """
    Define o tipo de compromisso do parlamentar.
    Ex.: Reunião, Evento festivo, Etc.
    """
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    ativo = models.BooleanField(default=True)

    objects = DeputadoManager()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipo de compromisso'
        verbose_name_plural = 'Tipos de compromisso'
        ordering = ('nome',)


class Compromisso(models.Model):
    """
    Define o compromisso com os dados do evento, isso será exibido no relatório de roteiros.
    """
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    data = models.DateField()
    hora_inicio = models.TimeField('Horário de início', unique_for_date='data')
    hora_fim = models.TimeField('Horário de término', unique_for_date='data')
    tipo = models.ForeignKey('TipoCompromisso', on_delete=models.PROTECT,
                             help_text='Define o tipo de compromisso do parlamentar. Ex.: Reunião, Evento festivo, Etc.')
    local = models.CharField(max_length=60, help_text='Local do evento')
    descricao = models.TextField('Descrição',
                                 help_text='Descrição geral do evento, para que o parlamentar saiba do que se trata.')
    obs = models.TextField('Observações', blank=True, null=True)

    def __str__(self):
        '{} em {} das {}h às {}h'.format(self.tipo, self.local, self.hora_inicio.strftime('%H:%i'),
                                         self.hora_fim.strftime('%H:%i'))

    class Meta:
        ordering = ('data', 'hora_inicio')


class Companhia(models.Model):
    """
    Companhias aéreas
    """
    nome = models.CharField(max_length=60)
    ativo = models.BooleanField(default=True)

    objects = DeputadoManager()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Companhia aérea'
        verbose_name_plural = 'Companhias aéreas'
        ordering = ('nome',)


class Voo(models.Model):
    """
    Informações sobre os vôos marcados, isso será exibido no relatório de roteiros.
    """
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    cidade_partida = models.ForeignKey('gabinete.Cidade', on_delete=models.PROTECT, verbose_name='Cidade de partida',
                                       related_name='cidade_partida_voo')
    data_hora_partida = models.DateTimeField('Data e horário de partida')
    cidade_chegada = models.ForeignKey('gabinete.Cidade', on_delete=models.PROTECT, verbose_name='Cidade de chegada',
                                       related_name='cidade_chegada_voo')
    data_hora_chegada = models.DateTimeField('Data e horário de chegada')
    companhia = models.ForeignKey('Companhia', on_delete=models.PROTECT, verbose_name='Companhia aérea')
    localizador = models.CharField(max_length=60, help_text='Código localizador do vôo.')
    numero = models.PositiveIntegerField('Número do vôo')
    portao = models.CharField('Portão de embarque', max_length=30)
    assento = models.PositiveIntegerField('Número do assento')
    obs = models.TextField('Observações', blank=True, null=True)

    def __str__(self):
        return 'Vôo {} pela {} saindo de {} dia {}h com chegada em {} dia {}h'.format(self.numero,
                                                                                      self.companhia,
                                                                                      self.cidade_partida,
                                                                                      self.data_hora_partida
                                                                                      .strftime('%D %d/%m/%Y %H:%i'),
                                                                                      self.cidade_chegada,
                                                                                      self.data_hora_chegada
                                                                                      .strftime('%D %d/%m/%Y %H:%i'))

    class Meta:
        verbose_name = 'Vôo'
        verbose_name_plural = 'Vôos'
        ordering = ('data_hora_partida',)