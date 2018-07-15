from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from gabinete.models import DeputadoManager


class PessoaManager(DeputadoManager):
    def ativos(self, deputado=None, *args, **kwargs):
        hoje = timezone.now().date()
        return self.ativo(deputado=deputado, fim_mandato__gte=hoje, *args, **kwargs)


class Cargo(models.Model):
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    ativo = models.BooleanField(default=True)

    objects = DeputadoManager()

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

class Instituicao(models.Model):
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    cidade = models.ForeignKey('gabinete.Cidade', on_delete=models.PROTECT)
    regional = models.ForeignKey('gabinete.Regional', on_delete=models.PROTECT,
                                    help_text='Regional a qual pertence a instituição.')


class Pessoa(models.Model):
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    pronome = models.CharField(max_length=2, choices=[('À', 'À'), ('Ao', 'Ao')],
                               help_text='Utilizado na emissão de documentos.')
    tratamento = models.CharField(max_length=60, null=True, blank=True,
                                  help_text='Pronome de tratamento incluído nos documentos emitidos. Ex.: Vossa Excelência o Sr.')
    nome = models.CharField(max_length=60)
    instituicao = models.ForeignKey('Instituicao', on_delete=models.PROTECT, blank=True, null=True,
                                 help_text='Instituição em qual a pessoa trabalha.')
    cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT, blank=True, null=True,
                              help_text='Cargo que a pessoa trabalha.')
    partido = models.ForeignKey('gabinete.Partido', on_delete=models.PROTECT, blank=True, null=True)
    inicio_mandato = models.DateField('Início do mandato', null=True, blank=True)
    fim_mandato = models.DateField('Fim do mandato', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    objects = PessoaManager()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ('nome',)


class TelefonePessoa(models.Model):
    pessoa = models.ForeignKey('Pessoa', on_delete=models.PROTECT)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    obs = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.telefone

    class Meta:
        verbose_name = 'Contato de Pessoa'
        verbose_name_plural = 'Contatos de Pessoas'


class EmailPessoa(models.Model):
    pessoa = models.ForeignKey('Pessoa', on_delete=models.PROTECT)
    email = models.CharField(max_length=100, blank=True, null=True)
    obs = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.telefone

    class Meta:
        verbose_name = 'E-mail de Pessoa'
        verbose_name_plural = 'E-mail de Pessoas'


class EnderecoPessoa(models.Model):
    pessoa = models.ForeignKey('Pessoa', on_delete=models.PROTECT)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=100, help_text='Nome da rua ou avenida.')
    numero = models.CharField('Número', max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.ForeignKey('gabinete.Cidade', on_delete=models.PROTECT)

    def __str__(self):
        return self.cep

    class Meta:
        verbose_name = 'Emdereço de Pessoa'
        verbose_name_plural = 'Endereço de Pessoas'
        ordering = ('cidade',)


class Oficio(models.Model):
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    data = models.DateField()
    regional = models.ForeignKey('gabinete.Regional', on_delete=models.PROTECT)
    assunto = models.CharField(max_length=100)
    descricao = RichTextField('Descrição')

    objects = DeputadoManager()

    def __str__(self):
        return self.assunto

    class Meta:
        verbose_name = 'Ofício'
        verbose_name_plural = 'Ofícios'
        ordering = ('-data', 'assunto')


class EnvioOficio(models.Model):
    oficio = models.ForeignKey('Oficio', verbose_name='Ofício', on_delete=models.CASCADE)
    enviado = models.BooleanField(default=False)
    erros = models.TextField(null=True, blank=True)
    data_hora_envio = models.DateTimeField('Data e hora de envio')

    def __str__(self):
        return 'Envio do Ofício {}'.format(self.oficio)

    class Meta:
        verbose_name = 'Envio do Ofício'
        verbose_name_plural = 'Envios dos Ofícios'