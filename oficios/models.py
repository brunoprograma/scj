from django.db import models
from django.utils import timezone
from gabinete.models import DeputadoManager


class EntidadeManager(DeputadoManager):
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


class Entidade(models.Model):
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    pronome = models.CharField(max_length=2, choices=[('À', 'À'), ('Ao', 'Ao')],
                               help_text='Utilizado na emissão de documentos.')
    tratamento = models.CharField(max_length=60, null=True, blank=True,
                                  help_text='Pronome de tratamento incluído nos documentos emitidos. Ex.: Vossa Excelência o Sr.')
    nome = models.CharField(max_length=60)
    regional = models.ForeignKey('gabinete.Regional', on_delete=models.PROTECT,
                                 help_text='Regional a qual pertence a pessoa ou entidade.')
    cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT, blank=True, null=True)
    partido = models.ForeignKey('gabinete.Partido', on_delete=models.PROTECT, blank=True, null=True)
    logradouro = models.CharField(max_length=100, help_text='Nome da rua ou avenida.')
    numero = models.CharField('Número', max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.ForeignKey('gabinete.Cidade', on_delete=models.PROTECT)
    inicio_mandato = models.DateField('Início do mandato', null=True, blank=True)
    fim_mandato = models.DateField('Fim do mandato', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    objects = EntidadeManager()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Pessoa ou Entidade'
        verbose_name_plural = 'Pessoas ou Entidades'
        ordering = ('nome',)


class ContatoEntidade(models.Model):
    entidade = models.ForeignKey('Entidade', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    celular = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Contato de Pessoa ou Entidade'
        verbose_name_plural = 'Contatos de Pessoa ou Entidade'
        ordering = ('nome',)


class Oficio(models.Model): #O numero vai ser o ID concatenado com o GDVC
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    data = models.DateField()
    regional = models.ForeignKey('gabinete.Regional', on_delete=models.PROTECT)
    assunto = models.CharField(max_length=100)
    descricao = models.TextField('Descrição')

    objects = DeputadoManager()

    def __str__(self):
        return self.assunto

    class Meta:
        verbose_name = 'Ofício'
        verbose_name_plural = 'Ofícios'
        ordering = ('-data', 'assunto')