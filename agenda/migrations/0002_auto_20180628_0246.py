# Generated by Django 2.0.6 on 2018-06-28 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gabinete', '0001_initial'),
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voo',
            name='cidade_chegada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cidade_chegada_voo', to='gabinete.Cidade', verbose_name='Cidade de chegada'),
        ),
        migrations.AddField(
            model_name='voo',
            name='cidade_partida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cidade_partida_voo', to='gabinete.Cidade', verbose_name='Cidade de partida'),
        ),
        migrations.AddField(
            model_name='voo',
            name='companhia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='agenda.Companhia', verbose_name='Companhia aérea'),
        ),
        migrations.AddField(
            model_name='voo',
            name='deputado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gabinete.Deputado'),
        ),
        migrations.AddField(
            model_name='tipocompromisso',
            name='deputado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gabinete.Deputado'),
        ),
        migrations.AddField(
            model_name='compromisso',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gabinete.Cidade'),
        ),
        migrations.AddField(
            model_name='compromisso',
            name='deputado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gabinete.Deputado'),
        ),
        migrations.AddField(
            model_name='compromisso',
            name='tipo',
            field=models.ForeignKey(help_text='Define o tipo de compromisso do parlamentar. Ex.: Reunião, Evento festivo, Etc.', on_delete=django.db.models.deletion.PROTECT, to='agenda.TipoCompromisso'),
        ),
    ]
