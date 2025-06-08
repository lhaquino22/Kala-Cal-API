"""
Serviços para cálculo de probabilidade de morte em pacientes com Kala-azar
Baseado nos algoritmos originais desenvolvidos em PHP
"""
from typing import Tuple

class KalaCalService:
    """
    Serviço que implementa os algoritmos de cálculo de probabilidade de morte
    para pacientes com Kala-azar baseado em dados epidemiológicos de Teresina-PI (2005-2013)
    """
    
    @staticmethod
    def limitar_casas_decimais(numero: float, casas: int = 3) -> float:
        """Limita o número de casas decimais"""
        return round(numero, casas)
    
    @staticmethod
    def prob_morte_maior_2anos_clinico(escore: int) -> float:
        """
        Modelo Clínico para pacientes > 2 anos
        """
        probabilidades = {
            0: 0.003338385,
            1: 0.007394025,
            2: 0.016296045,
            3: 0.035531694,
            4: 0.075723719,
            5: 0.154109282,
            6: 0.288305571,
            7: 0.47384157,
            8: 0.666793942,
            9: 0.816254194,
            10: 0.907745889,  # estimada
            11: 0.955925539,
            12: 0.979297619,  # estimada
            13: 0.9901837219,  # estimada
        }
        return KalaCalService.limitar_casas_decimais(probabilidades.get(escore, 0.0))
    
    @staticmethod
    def prob_morte_maior_2anos_clinico_laboratorial(escore: int) -> float:
        """
        Modelo Clínico e Laboratorial para pacientes > 2 anos
        """
        probabilidades = {
            0: 0.000296031,
            1: 0.002497884,
            2: 0.016670987,
            3: 0.07829276,
            4: 0.239717557,
            5: 0.488427303,
            6: 0.732603013,
            7: 0.907305187,
            8: 1.010570531,
            9: 1.065581353,
            10: 1.093365948,
        }
        return KalaCalService.limitar_casas_decimais(probabilidades.get(escore, 0.0))
    
    @staticmethod
    def prob_morte_menor_2anos_clinico(escore: int) -> float:
        """
        Modelo Clínico para pacientes < 2 anos
        """
        probabilidades = {
            0: 0.000966832,
            1: 0.011300207,
            2: 0.030329499,
            3: 0.064934076,
            4: 0.127411596,
            5: 0.239744118,
            6: 0.441223098,
            7: 0.802077796,
            8: 1.447833833,
            9: 2.602850084,
        }
        return KalaCalService.limitar_casas_decimais(probabilidades.get(escore, 0.0))
    
    @staticmethod
    def prob_morte_menor_2anos_clinico_laboratorial(escore: int) -> float:
        """
        Modelo Clínico e Laboratorial para pacientes < 2 anos
        """
        probabilidades = {
            0: 0.001228266,
            1: 0.003789667,
            2: 0.011090773,
            3: 0.030042234,
            4: 0.073187025,
            5: 0.156050276,
            6: 0.286334983,
            7: 0.45223825,
            8: 0.62553836,
            9: 0.778752936,
            10: 0.897964538,
            11: 0.982676514,
        }
        return KalaCalService.limitar_casas_decimais(probabilidades.get(escore, 0.0))
    
    @staticmethod
    def calcular_escore_clinico_crianca(dados: dict) -> int:
        """
        Calcula o escore clínico para crianças (< 2 anos)
        """
        escore = 0
        
        # Idade
        if dados.get('faixa_etaria') == 1:  # < 12 meses
            escore += 1
        # 12-23 meses não adiciona pontos
        
        # Sítios de sangramento
        sangramento = dados.get('sitios_sangramento', 1)
        if sangramento == 2:  # 1-2 sítios
            escore += 1
        elif sangramento == 3:  # 3-4 sítios
            escore += 2
        elif sangramento == 4:  # 5-6 sítios
            escore += 4
        
        # Sinais clínicos
        if dados.get('ictericia', False):
            escore += 1
        if dados.get('dispneia', False):
            escore += 1
        if dados.get('edema', False):
            escore += 2
        
        return escore
    
    @staticmethod
    def calcular_escore_laboratorial_crianca(dados: dict) -> int:
        """
        Calcula o escore laboratorial para crianças (< 2 anos)
        """
        escore = 0
        
        # Idade
        if dados.get('faixa_etaria') == 1:  # < 12 meses
            escore += 1
        
        # Sítios de sangramento
        sangramento = dados.get('sitios_sangramento', 1)
        if sangramento == 2:  # 1-2 sítios
            escore += 1
        elif sangramento == 3:  # 3-4 sítios
            escore += 2
        elif sangramento == 4:  # 5-6 sítios
            escore += 4
        
        # Sinais clínicos (não usa icterícia no modelo laboratorial)
        if dados.get('dispneia', False):
            escore += 1
        if dados.get('edema', False):
            escore += 2
        if dados.get('hepatite', False):
            escore += 3  # exclusivo do laboratorial
        
        return escore
    
    @staticmethod
    def calcular_escore_clinico_adulto(dados: dict) -> int:
        """
        Calcula o escore clínico para adultos (>= 2 anos)
        """
        escore = 0
        
        # Idade
        faixa_etaria = dados.get('faixa_etaria', 3)
        if faixa_etaria == 4:  # 16-40 anos
            escore += 2
        elif faixa_etaria == 5:  # > 40 anos
            escore += 3
        
        # Sítios de sangramento
        sangramento = dados.get('sitios_sangramento', 1)
        if sangramento == 4:  # 5-6 sítios
            escore += 3
        
        # Sinais clínicos
        if dados.get('aids', False):
            escore += 2
        if dados.get('edema', False):
            escore += 1
        if dados.get('ictericia', False):
            escore += 1
        if dados.get('dispneia', False):
            escore += 1
        if dados.get('infeccao', False):
            escore += 1
        if dados.get('vomitos', False):
            escore += 1
        
        return escore
    
    @staticmethod
    def calcular_escore_laboratorial_adulto(dados: dict) -> int:
        """
        Calcula o escore laboratorial para adultos (>= 2 anos)
        """
        escore = 0
        
        # Idade não influencia no modelo laboratorial adulto
        # Sítios de sangramento não influenciam no modelo laboratorial adulto
        
        # Sinais clínicos
        if dados.get('aids', False):
            escore += 2
        # edema não pontua no modelo laboratorial adulto
        if dados.get('ictericia', False):
            escore += 1
        if dados.get('dispneia', False):
            escore += 1
        if dados.get('infeccao', False):
            escore += 1
        # vomitos não pontua no modelo laboratorial adulto
        
        # Dados laboratoriais
        if dados.get('leucopenia', False):
            escore += 1
        if dados.get('plaquetopenia', False):
            escore += 2
        if dados.get('insuficiencia_renal', False):
            escore += 2
        
        return escore
    
    @classmethod
    def calcular_probabilidade(cls, dados: dict, modelo: str = 'clinico') -> Tuple[int, float]:
        """
        Calcula a probabilidade de morte baseada nos dados do paciente
        
        Args:
            dados: Dicionário com dados do paciente
            modelo: 'clinico' ou 'clinico_laboratorial'
        
        Returns:
            Tupla (escore, probabilidade_morte)
        """
        faixa_etaria = dados.get('faixa_etaria')
        is_crianca = faixa_etaria in [1, 2]  # < 2 anos
        
        # Calcular escore baseado na idade e modelo
        if is_crianca:
            if modelo == 'clinico':
                escore = cls.calcular_escore_clinico_crianca(dados)
                probabilidade = cls.prob_morte_menor_2anos_clinico(escore)
            else:  # clinico_laboratorial
                escore = cls.calcular_escore_laboratorial_crianca(dados)
                probabilidade = cls.prob_morte_menor_2anos_clinico_laboratorial(escore)
        else:  # adulto
            if modelo == 'clinico':
                escore = cls.calcular_escore_clinico_adulto(dados)
                probabilidade = cls.prob_morte_maior_2anos_clinico(escore)
            else:  # clinico_laboratorial
                escore = cls.calcular_escore_laboratorial_adulto(dados)
                probabilidade = cls.prob_morte_maior_2anos_clinico_laboratorial(escore)
        
        # Converter para porcentagem
        probabilidade_porcentagem = probabilidade * 100
        
        return escore, cls.limitar_casas_decimais(probabilidade_porcentagem, 1) 