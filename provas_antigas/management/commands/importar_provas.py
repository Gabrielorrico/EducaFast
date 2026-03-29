from django.core.management.base import BaseCommand
import os
from provas_antigas.models import Prova


class Command(BaseCommand):
    help = 'Importa provas automaticamente'

    def handle(self, *args, **kwargs):
        pasta = 'media/provas_pdf'

        for nome_arquivo in os.listdir(pasta):
            if nome_arquivo.endswith('.pdf'):
                try:
                    partes = nome_arquivo.replace('.pdf', '').split('_')

                    ano    = int(partes[0])
                    edicao = partes[1] if len(partes) > 1 else 'desconhecida'
                    tipo   = partes[2] if len(partes) > 2 else 'desconhecido'
                    area   = partes[3] if len(partes) > 3 else 'geral'

                    if Prova.objects.filter(pdf_prova=f'provas_pdf/{nome_arquivo}').exists():
                        self.stdout.write(f'⚠ {nome_arquivo} já importado, pulando...')
                        continue

                    Prova.objects.create(
                        ano=ano,
                        edicao=edicao,
                        tipo=tipo,
                        area_conhecimento=area,
                        total_questoes=45,
                        pdf_prova=f'provas_pdf/{nome_arquivo}'
                    )
                    self.stdout.write(self.style.SUCCESS(f'✔ {nome_arquivo} importado'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Erro em {nome_arquivo}: {e}'))