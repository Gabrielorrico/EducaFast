import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('icone', models.CharField(choices=[('📐', 'Matemática'), ('📖', 'Língua Portuguesa'), ('✍️', 'Redação'), ('🌎', 'Ciências Humanas'), ('🔬', 'Ciências da Natureza')], default='📐', max_length=10)),
                ('classe_css', models.CharField(blank=True, max_length=50)),
                ('ordem', models.PositiveSmallIntegerField(default=0, help_text='Ordem de exibição')),
            ],
            options={
                'verbose_name': 'Matéria',
                'verbose_name_plural': 'Matérias',
                'ordering': ['ordem'],
            },
        ),
        migrations.CreateModel(
            name='Topico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('ordem', models.PositiveSmallIntegerField(default=0, help_text='Ordem de exibição')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicos', to='assuntos_recorrentes.materia')),
            ],
            options={
                'verbose_name': 'Tópico',
                'verbose_name_plural': 'Tópicos',
                'ordering': ['ordem'],
            },
        ),
        migrations.CreateModel(
            name='TopicoMarcado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marcado_em', models.DateTimeField(auto_now_add=True)),
                ('topico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marcacoes', to='assuntos_recorrentes.topico')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicos_marcados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tópico Marcado',
                'verbose_name_plural': 'Tópicos Marcados',
                'unique_together': {('usuario', 'topico')},
            },
        ),
    ]
