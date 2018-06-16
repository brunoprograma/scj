from .models import EnvioOficio


def envia_oficios():
    for envio in EnvioOficio.objects.filter(enviado=False):
        pass # envia os oficios
