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
    cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT, blank=True, null=True)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    whatsapp = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()


class Partido(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    sigla = models.CharField(max_length=30)
    ativo = models.BooleanField(default=True)


class Regional(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    ativa = models.BooleanField(default=True)


class Cargo(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    ativo = models.BooleanField(default=True)


class Entidade(models.Model):
    pronome = models.CharField(max_length=2, choices=[('À', 'À'), ('Ao', 'Ao')])
    tratamento = models.CharField(max_length=60, null=True, blank=True)
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    regional = models.ForeignKey('Regional', on_delete=models.PROTECT)
    cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT, blank=True, null=True)
    partido = models.ForeignKey('Partido', on_delete=models.PROTECT, blank=True, null=True)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT)
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
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    data = models.DateField()
    regional = models.ForeignKey('Regional', on_delete=models.PROTECT)
    assunto = models.CharField(max_length=100)
    descricao = models.TextField('Descrição')


class TipoCompromisso(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    ativo = models.BooleanField(default=True)


class Compromisso(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    tipo = models.ForeignKey('TipoCompromisso', on_delete=models.PROTECT)
    local = models.CharField(max_length=60)
    descricao = models.TextField('Descrição')
    obs = models.TextField('Observações', blank=True, null=True)


class Companhia(models.Model):
    nome = models.CharField(max_length=60)
    ativa = models.BooleanField(default=True)


class Voo(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    cidade_partida = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    data_hora_partida = models.DateTimeField()
    cidade_chegada = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    data_hora_chegada = models.DateTimeField()
    companhia = models.ForeignKey('Companhia', on_delete=models.PROTECT)
    localizador = models.CharField(max_length=60)
    numero = models.PositiveIntegerField('Número do vôo')
    portao = models.CharField('Portão de embarque', max_length=30)
    assento = models.PositiveIntegerField('Número do assento')
    obs = models.TextField('Observações', blank=True, null=True)