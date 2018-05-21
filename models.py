from django.db import models


class Estado(models.Model):
    nome = models.CharField(max_length=60)
    sigla = models.CharField(max_length=2)


class Cidade(models.Model):
    nome = models.CharField(max_length=60)
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT)


class Deputado(models.Model):
    # TODO: dados do deputado, endereços e contatos
    nome = models.CharField(max_length=60)
    ativo = models.BooleanField(default=True)


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
    # TODO: especificações de gênero e tratamento
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    regional = models.ForeignKey('Regional', on_delete=models.PROTECT)
    cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT, blank=True, null=True)
    partido = models.ForeignKey('Partido', on_delete=models.PROTECT, blank=True, null=True)
    inicio_mandato = models.DateField('Início do mandato', null=True, blank=True)
    fim_mandato = models.DateField('Fim do mandato', null=True, blank=True)
    ativo = models.BooleanField(default=True)


class ContatoEntidade(models.Model):
    # TODO: verificar se contatos tem que ser separados de endereços
    entidade = models.ForeignKey('Entidade', on_delete=models.PROTECT)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    whatsapp = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()


class Oficio(models.Model):
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    data_emissao = models.DateField('Data de emissão')
    numero = models.CharField(max_length=60)
    regional = models.ForeignKey('Regional', on_delete=models.PROTECT)
    assunto = models.CharField(max_length=100)
    descricao = models.TextField('Descrição')


# TODO: verificar situação dos roteiros, vôos e compromissos
class Roteiros(models.Model):
    id = models.IntegerField(db_column='ID', unique=True)
    data_hora_inicial = models.DateTimeField(db_column='Data_Hora_Inicial')
    data_hora_final = models.DateTimeField(db_column='Data_Hora_Final')
    id_tipo = models.IntegerField(db_column='ID_Tipo')
    local = models.CharField(db_column='Local', max_length=45, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=255)
    obs = models.CharField(db_column='Obs', max_length=255, blank=True, null=True)
    id_deputado = models.IntegerField(db_column='ID_Deputado')


class Tipos(models.Model):
    id = models.IntegerField(db_column='ID', unique=True)
    tipo = models.CharField(db_column='Tipo', max_length=45)
    id_deputado = models.IntegerField(db_column='ID_Deputado')
    ativo = models.BooleanField(default=True)


class Viagem(models.Model):
    id = models.IntegerField(db_column='ID', unique=True)
    obs = models.CharField(db_column='Obs', max_length=255, blank=True, null=True)
    id_deputado = models.IntegerField(db_column='ID_Deputado')


class Companhia(models.Model):
    nome = models.CharField(max_length=60)
    ativa = models.BooleanField(default=True)


class Voos(models.Model):
    id = models.IntegerField(db_column='ID', unique=True)
    id_viagem = models.IntegerField(db_column='ID_Viagem')
    id_cidade_partida = models.IntegerField(db_column='ID_Cidade_Partida')
    id_cidade_chegada = models.IntegerField(db_column='ID_Cidade_Chegada')
    data_hora_partida = models.DateTimeField(db_column='Data_Hora_Partida')
    data_hora_chegada = models.DateTimeField(db_column='Data_Hora_Chegada')
    id_companhia = models.IntegerField(db_column='ID_Companhia')
    localizador = models.CharField(db_column='Localizador', max_length=45)
    numero_voo = models.IntegerField(db_column='Numero_Voo')
    assento = models.IntegerField(db_column='Assento')
    id_deputado = models.IntegerField(db_column='ID_Deputado')