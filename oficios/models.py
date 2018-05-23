from django.db import models


class Cargo(models.Model):
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    ativo = models.BooleanField(default=True)


class Entidade(models.Model):
    pronome = models.CharField(max_length=2, choices=[('À', 'À'), ('Ao', 'Ao')])
    tratamento = models.CharField(max_length=60, null=True, blank=True)
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    regional = models.ForeignKey('gabinete.Regional', on_delete=models.PROTECT)
    cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT, blank=True, null=True)
    partido = models.ForeignKey('gabinete.Partido', on_delete=models.PROTECT, blank=True, null=True)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.ForeignKey('gabinete.Cidade', on_delete=models.PROTECT)
    inicio_mandato = models.DateField('Início do mandato', null=True, blank=True)
    fim_mandato = models.DateField('Fim do mandato', null=True, blank=True)
    ativo = models.BooleanField(default=True)


class ContatoEntidade(models.Model):
    entidade = models.ForeignKey('Entidade', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    whatsapp = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()


class Oficio(models.Model):
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT)
    cidade = models.ForeignKey('gabinete.Cidade', on_delete=models.PROTECT)
    data = models.DateField()
    regional = models.ForeignKey('gabinete.Regional', on_delete=models.PROTECT)
    assunto = models.CharField(max_length=100)
    descricao = models.TextField('Descrição')
