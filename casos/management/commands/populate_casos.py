from django.core.management.base import BaseCommand
from django.utils import timezone
from casos.models import Caso
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Popula o banco de dados com casos de exemplo'

    def handle(self, *args, **options):
        # Limpa os dados existentes
        Caso.objects.all().delete()
        
        # Dados de exemplo
        municipios = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Fortaleza', 'Brasília']
        
        casos_exemplo = [
            {
                'identificador': 'H001',
                'tipo_caso': 'humano',
                'sexo': 'masculino',
                'gestante': False,
                'municipio': 'São Paulo',
                'latitude': -23.5505,
                'longitude': -46.6333,
            },
            {
                'identificador': 'H002',
                'tipo_caso': 'humano',
                'sexo': 'feminino',
                'gestante': True,
                'municipio': 'Rio de Janeiro',
                'latitude': -22.9068,
                'longitude': -43.1729,
            },
            {
                'identificador': 'A001',
                'tipo_caso': 'animal',
                'sexo': 'masculino',
                'gestante': False,
                'municipio': 'Belo Horizonte',
                'latitude': -19.9191,
                'longitude': -43.9386,
            },
            {
                'identificador': 'H003',
                'tipo_caso': 'humano',
                'sexo': 'feminino',
                'gestante': False,
                'municipio': 'Salvador',
                'latitude': -12.9714,
                'longitude': -38.5014,
            },
            {
                'identificador': 'A002',
                'tipo_caso': 'animal',
                'sexo': 'feminino',
                'gestante': True,
                'municipio': 'Fortaleza',
                'latitude': -3.7319,
                'longitude': -38.5267,
            },
        ]
        
        # Cria os casos
        for caso_data in casos_exemplo:
            # Gera uma data aleatória nos últimos 30 dias
            data_notificacao = date.today() - timedelta(days=random.randint(1, 30))
            data_nascimento = date.today() - timedelta(days=random.randint(365*5, 365*60))  # Entre 5 e 60 anos
            
            caso = Caso.objects.create(
                identificador=caso_data['identificador'],
                tipo_caso=caso_data['tipo_caso'],
                sexo=caso_data['sexo'],
                gestante=caso_data['gestante'],
                data_notificacao=data_notificacao,
                data_nascimento=data_nascimento,
                municipio=caso_data['municipio'],
                latitude=caso_data['latitude'],
                longitude=caso_data['longitude'],
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Caso criado: {caso.identificador} - {caso.municipio}')
            )
        
        # Cria mais alguns casos aleatórios
        for i in range(10):
            identificador = f"{'H' if random.choice([True, False]) else 'A'}{100 + i:03d}"
            tipo_caso = 'humano' if identificador.startswith('H') else 'animal'
            sexo = random.choice(['masculino', 'feminino'])
            gestante = sexo == 'feminino' and random.choice([True, False])
            municipio = random.choice(municipios)
            
            # Coordenadas aproximadas do Brasil
            latitude = random.uniform(-33.75, 5.27)
            longitude = random.uniform(-73.99, -34.79)
            
            data_notificacao = date.today() - timedelta(days=random.randint(1, 60))
            data_nascimento = date.today() - timedelta(days=random.randint(365*1, 365*80))
            
            Caso.objects.create(
                identificador=identificador,
                tipo_caso=tipo_caso,
                sexo=sexo,
                gestante=gestante,
                data_notificacao=data_notificacao,
                data_nascimento=data_nascimento,
                municipio=municipio,
                latitude=latitude,
                longitude=longitude,
            )
        
        total_casos = Caso.objects.count()
        humanos = Caso.objects.filter(tipo_caso='humano').count()
        animais = Caso.objects.filter(tipo_caso='animal').count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nDados populados com sucesso!\n'
                f'Total de casos: {total_casos}\n'
                f'Casos humanos: {humanos}\n'
                f'Casos animais: {animais}'
            )
        ) 