from django.db import models


class Pais(models.Model):
    nome = models.CharField(max_length=60)


class Estado(models.Model):
    nome = models.CharField(max_length=60)
    sigla = models.CharField(max_length=2)
    pais = models.ForeignKey('Pais', on_delete=models.PROTECT)


class Cidade(models.Model):
    nome = models.CharField(max_length=60)
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT)


class Deputado(models.Model):
    genero = models.CharField('Gênero', max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    tratamento = models.CharField(max_length=60, blank=True, null=True)
    nome = models.CharField(max_length=60)
    partido = models.ForeignKey('Partido', on_delete=models.PROTECT)
    mensagem = models.CharField(max_length=60, null=True, blank=True)
    ativo = models.BooleanField(default=True)


class EnderecoDeputado(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    whatsapp = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()


class Partido(models.Model):
    nome = models.CharField(max_length=60)
    sigla = models.CharField(max_length=30)
    ativo = models.BooleanField(default=True)


class Regional(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    ativa = models.BooleanField(default=True)
