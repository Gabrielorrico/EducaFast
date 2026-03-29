from django.core.management.base import BaseCommand
import os
from provas_antigas.models import Prova


LINKS_PDF = {
    '2022_1dia_azul_humanas': 'https://download.inep.gov.br/enem/provas_e_gabaritos/2022_PV_impresso_D1_CD1.pdf',
    '2022_1dia_regular': 'https://download.inep.gov.br/enem/provas_e_gabaritos/2022_PV_impresso_D1_CD4.pdf',
    '2022_2dia_azul_matematica': 'https://download.inep.gov.br/enem/provas_e_gabaritos/2022_PV_impresso_D2_CD7.pdf',
    '2024_1dia_azul_humanas': 'https://download.inep.gov.br/enem/provas_e_gabaritos/2024_PV_impresso_D1_CD1.pdf',
    '2024_2dia_azul_matematica': 'https://download.inep.gov.br/enem/provas_e_gabaritos/2024_PV_impresso_D2_CD7.pdf',
    '2025_PV_impresso_D1_CD1': 'https://download.inep.gov.br/enem/provas_e_gabaritos/2025_PV_impresso_D1_CD4.pdf',
}


class Command(BaseCommand):
    help = 'Importa provas automaticamente'

    def handle(self, *args, **kwargs):
        pasta = 'media/provas_pdf'

        for nome_arquivo in os.listdir(pasta):
            if nome_arquivo.endswith('.pdf'):
                try:
                    nome_sem_ext = nome_arquivo.replace('.pdf', '')
                    partes = nome_sem_ext.split('_')

                    ano    = int(partes[0])
                    edicao = partes[1] if len(partes) > 1 else 'desconhecida'
                    tipo   = partes[2] if len(partes) > 2 else 'desconhecido'
                    area   = partes[3] if len(partes) > 3 else 'geral'

                    pdf_url = LINKS_PDF.get(nome_sem_ext, '')

                    if Prova.objects.filter(ano=ano, edicao=edicao, tipo=tipo).exists():
                        self.stdout.write(f'⚠ {nome_arquivo} já importado, pulando...')
                        continue

                    Prova.objects.create(
                        ano=ano,
                        edicao=edicao,
                        tipo=tipo,
                        area_conhecimento=area,
                        total_questoes=45,
                        pdf_url=pdf_url,
                    )
                    self.stdout.write(self.style.SUCCESS(f'✔ {nome_arquivo} importado'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Erro em {nome_arquivo}: {e}'))