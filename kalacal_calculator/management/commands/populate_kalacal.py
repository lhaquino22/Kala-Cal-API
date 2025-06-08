from django.core.management.base import BaseCommand
from kalacal_calculator.models import CalculoKalaCal
from kalacal_calculator.services import KalaCalService
from casos.models import Caso, FaixaEtaria, SitiosSangramento

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo do KalaCal usando casos existentes'

    def handle(self, *args, **options):
        self.stdout.write('Populando dados de exemplo do KalaCal...')

        # Limpar cálculos existentes
        CalculoKalaCal.objects.all().delete()

        # Verificar se temos casos para trabalhar
        casos_existentes = Caso.objects.count()
        if casos_existentes == 0:
            self.stdout.write(
                self.style.WARNING('Nenhum caso encontrado. Execute primeiro "python manage.py populate_casos"')
            )
            return

        # Dados de exemplo para casos KalaCal
        casos_kalacal_exemplo = [
            {
                'identificador': 'KALA001',
                'tipo_caso': 'humano',
                'sexo': 'feminino',
                'data_nascimento': '2024-01-15',  # < 12 meses
                'municipio': 'Teresina',
                'kalacal_habilitado': True,
                'faixa_etaria_kalacal': FaixaEtaria.MENOR_12M,
                'sitios_sangramento': SitiosSangramento.UM_DOIS,
                'edema': True,
                'dispneia': False,
                'ictericia': True,
            },
            {
                'identificador': 'KALA002',
                'tipo_caso': 'humano',
                'sexo': 'masculino',
                'data_nascimento': '2023-06-10',  # 12-23 meses
                'municipio': 'Teresina',
                'kalacal_habilitado': True,
                'faixa_etaria_kalacal': FaixaEtaria.ENTRE_12_23M,
                'sitios_sangramento': SitiosSangramento.TRES_QUATRO,
                'edema': False,
                'dispneia': True,
                'ictericia': False,
                'hepatite': True,
            },
            {
                'identificador': 'KALA003',
                'tipo_caso': 'humano',
                'sexo': 'feminino',
                'data_nascimento': '2015-03-20',  # 2-15 anos
                'municipio': 'Teresina',
                'kalacal_habilitado': True,
                'faixa_etaria_kalacal': FaixaEtaria.ENTRE_2_15A,
                'sitios_sangramento': SitiosSangramento.NENHUM,
                'edema': False,
                'aids': False,
                'ictericia': False,
                'dispneia': True,
                'infeccao': False,
                'vomitos': False,
            },
            {
                'identificador': 'KALA004',
                'tipo_caso': 'humano',
                'sexo': 'masculino',
                'data_nascimento': '1990-08-15',  # 16-40 anos
                'municipio': 'Teresina',
                'kalacal_habilitado': True,
                'faixa_etaria_kalacal': FaixaEtaria.ENTRE_16_40A,
                'sitios_sangramento': SitiosSangramento.CINCO_SEIS,
                'edema': True,
                'aids': False,
                'ictericia': True,
                'dispneia': True,
                'infeccao': True,
                'vomitos': False,
                'leucopenia': True,
                'plaquetopenia': True,
                'insuficiencia_renal': False,
            },
            {
                'identificador': 'KALA005',
                'tipo_caso': 'humano',
                'sexo': 'feminino',
                'data_nascimento': '1975-12-01',  # > 40 anos
                'municipio': 'Teresina',
                'kalacal_habilitado': True,
                'faixa_etaria_kalacal': FaixaEtaria.MAIOR_40A,
                'sitios_sangramento': SitiosSangramento.TRES_QUATRO,
                'edema': False,
                'aids': True,
                'ictericia': False,
                'dispneia': False,
                'infeccao': True,
                'vomitos': True,
                'leucopenia': False,
                'plaquetopenia': True,
                'insuficiencia_renal': True,
            }
        ]

        # Criar casos e calcular probabilidades
        for i, dados_caso in enumerate(casos_kalacal_exemplo, 1):
            # Criar caso
            caso = Caso.objects.create(**dados_caso)
            self.stdout.write(f'Criado caso: {caso.identificador}')

            # Obter dados para cálculo
            dados_calculo = caso.get_dados_kalacal()
            
            # Calcular para modelo clínico
            escore_clinico, prob_clinico = KalaCalService.calcular_probabilidade(
                dados_calculo, 'clinico'
            )
            
            CalculoKalaCal.objects.create(
                caso=caso,
                modelo_usado='clinico',
                escore=escore_clinico,
                probabilidade_morte=prob_clinico,
                observacoes=f'Cálculo inicial para caso de exemplo {i}'
            )
            
            self.stdout.write(f'  Modelo clínico: Escore {escore_clinico}, Probabilidade {prob_clinico}%')

            # Calcular para modelo clínico+laboratorial (se tiver dados laboratoriais)
            tem_dados_lab = any(getattr(caso, campo, False) for campo in 
                              ['leucopenia', 'plaquetopenia', 'insuficiencia_renal', 'hepatite'])
            
            if tem_dados_lab or caso.is_crianca_kalacal():
                escore_lab, prob_lab = KalaCalService.calcular_probabilidade(
                    dados_calculo, 'clinico_laboratorial'
                )
                
                CalculoKalaCal.objects.create(
                    caso=caso,
                    modelo_usado='clinico_laboratorial',
                    escore=escore_lab,
                    probabilidade_morte=prob_lab,
                    observacoes=f'Cálculo laboratorial para caso de exemplo {i}'
                )
                
                self.stdout.write(f'  Modelo clínico+lab: Escore {escore_lab}, Probabilidade {prob_lab}%')

        # Estatísticas finais
        total_casos = Caso.objects.filter(kalacal_habilitado=True).count()
        total_calculos = CalculoKalaCal.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSucesso! Criados {total_casos} casos KalaCal e {total_calculos} cálculos de exemplo.'
            )
        ) 