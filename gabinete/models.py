from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class DeputadoManager(models.Manager):
    def ativo(self, deputado=None, *args, **kwargs):
        if deputado and ('deputado' in self.model._meta.get_fields(include_hidden=True)):
            return self.filter(ativo=True, deputado=deputado, *args, **kwargs)
        return self.filter(ativo=True, *args, **kwargs)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    deputado = models.ForeignKey('gabinete.Deputado', on_delete=models.PROTECT, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.username = self.email
        self.is_staff = True  # isso dá acesso ao ambiente de administração
        super().save(*args, **kwargs)


class Pais(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.title()
        super(Pais, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ('nome',)


class Estado(models.Model):
    nome = models.CharField(max_length=60)
    sigla = models.CharField(max_length=2)
    pais = models.ForeignKey('Pais', on_delete=models.PROTECT)

    def __str__(self):
        return self.sigla

    def save(self, *args, **kwargs):
        self.nome = self.nome.title()
        self.sigla = self.sigla.upper()
        super(Estado, self).save(*args, **kwargs)

    class Meta:
        ordering = ('sigla',)


class Cidade(models.Model):
    nome = models.CharField(max_length=60)
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT)

    def __str__(self):
        return '{}-{}'.format(self.nome, self.estado)

    def save(self, *args, **kwargs):
        self.nome = self.nome.title()
        super(Cidade, self).save(*args, **kwargs)

    class Meta:
        ordering = ('nome',)


class Partido(models.Model):
    nome = models.CharField(max_length=60)
    sigla = models.CharField(max_length=30)
    ativo = models.BooleanField(default=True)

    objects = DeputadoManager()

    def __str__(self):
        return self.sigla

    def save(self, *args, **kwargs):
        self.nome = self.nome.title()
        self.sigla = self.sigla.upper()
        super(Partido, self).save(*args, **kwargs)

    class Meta:
        ordering = ('sigla',)


class Deputado(models.Model):
    """
    Define as configurações do gabinete do parlamentar, utilizadas em relatórios e emissão de documentos.
    Essa classe representa a 'Empresa' e suas informações.
    """
    genero = models.CharField('Gênero', max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    tratamento = models.CharField('Pronome de tratamento', max_length=60, blank=True, null=True,
                                  help_text='Ex.: Dr., Sr., etc.')
    nome = models.CharField(max_length=60)
    abreviatura_oficio = models.CharField('Abreviatura do Ofício', max_length=10,
                                          help_text='Abreviatura de identificação inserida em todos os Ofícios.')
    partido = models.ForeignKey('Partido', on_delete=models.PROTECT)
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT, verbose_name='Estado de atuação')
    mensagem = models.CharField('Mensagem de assinatura', max_length=60, null=True, blank=True,
                                help_text='Exibida em documentos, junto à assinatura do parlamentar.')
    ativo = models.BooleanField(default=True)

    objects = DeputadoManager()

    def __str__(self):
        return '{} ({}-{})'.format(self.nome, self.partido, self.estado)

    @property
    def endereco_principal(self):
        if self.enderecodeputado_set.filter(principal=True).exists():
            return self.enderecodeputado_set.get(principal=True)
        return self.enderecodeputado_set.first() if self.enderecodeputado_set.all().exists() else None

    class Meta:
        verbose_name = 'Parlamentar'
        verbose_name_plural = 'Parlamentares'
        ordering = ('nome',)


class EnderecoDeputado(models.Model):
    """
    Escritório do parlamentar com suas informações de localização e contato.
    """
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    logradouro = models.CharField(max_length=100, help_text='Nome da rua ou avenida.')
    numero = models.CharField('Número', max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    telefone = models.CharField(max_length=30)
    fax = models.CharField(max_length=30, blank=True, null=True)
    celular = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()
    principal = models.BooleanField(default=False)

    def __str__(self):
        return '{}{} - {}{} {}'.format(self.logradouro,
                                       ', {}'.format(self.numero) if self.numero else '',
                                       self.bairro,
                                       ' {}'.format(self.complemento) if self.complemento else '',
                                       self.cidade)

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(EnderecoDeputado, self).save(*args, **kwargs)
        if self.principal:
            EnderecoDeputado.objects.exclude(id=self.pk).update(principal=False)

    class Meta:
        verbose_name = 'Endereço do parlamentar'
        verbose_name_plural = 'Endereços do parlamentar'
        ordering = ('id', )


class Regional(models.Model):
    """
    Regional é um agrupamento de Entidades (outros políticos ou organizações) definida pelo gabinete.
    """
    deputado = models.ForeignKey('Deputado', on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    ativo = models.BooleanField(default=True)

    objects = DeputadoManager()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Regional'
        verbose_name_plural = 'Regionais'
        ordering = ('nome',)