from django.db import models
from django.utils import timezone
from datetime import date

class TipoCaso(models.TextChoices):
    HUMANO = 'humano', 'Humano'
    ANIMAL = 'animal', 'Animal'

class Sexo(models.TextChoices):
    MASCULINO = 'masculino', 'Masculino'
    FEMININO = 'feminino', 'Feminino'

class FaixaEtaria(models.IntegerChoices):
    MENOR_12M = 1, '< 12 meses'
    ENTRE_12_23M = 2, '12-23 meses'
    ENTRE_2_15A = 3, '2-15 anos'
    ENTRE_16_40A = 4, '16-40 anos'
    MAIOR_40A = 5, '> 40 anos'

class SitiosSangramento(models.IntegerChoices):
    NENHUM = 1, 'Nenhum'
    UM_DOIS = 2, '1-2 sítios'
    TRES_QUATRO = 3, '3-4 sítios'
    CINCO_SEIS = 4, '5-6 sítios'

class Caso(models.Model):
    # Identificação
    identificador = models.CharField(max_length=50, unique=True)
    tipo_caso = models.CharField(max_length=10, choices=TipoCaso.choices)
    
    # Dados pessoais
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=Sexo.choices)
    gestante = models.BooleanField(default=False, null=True, blank=True)
    
    # Dados da notificação
    data_notificacao = models.DateField(default=date.today)
    
    # Localização
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    municipio = models.CharField(max_length=100, blank=True)
    
    # === CAMPOS ESPECÍFICOS PARA KALACAL ===
    # Faixa etária para cálculo (pode ser derivada da data_nascimento ou definida manualmente)
    faixa_etaria_kalacal = models.IntegerField(
        choices=FaixaEtaria.choices, 
        null=True, 
        blank=True,
        help_text="Faixa etária para cálculo KalaCal"
    )
    
    # Dados clínicos
    sitios_sangramento = models.IntegerField(
        choices=SitiosSangramento.choices, 
        null=True, 
        blank=True,
        help_text="Número de sítios de sangramento"
    )
    
    # Sinais e sintomas clínicos
    edema = models.BooleanField(default=False, help_text="Presença de edema")
    aids = models.BooleanField(default=False, help_text="Paciente com AIDS")
    ictericia = models.BooleanField(default=False, help_text="Presença de icterícia")
    dispneia = models.BooleanField(default=False, help_text="Presença de dispneia")
    infeccao = models.BooleanField(default=False, help_text="Presença de infecção")
    vomitos = models.BooleanField(default=False, help_text="Presença de vômitos")
    
    # Dados laboratoriais (opcionais)
    leucopenia = models.BooleanField(default=False, help_text="Presença de leucopenia")
    plaquetopenia = models.BooleanField(default=False, help_text="Presença de plaquetopenia")
    insuficiencia_renal = models.BooleanField(default=False, help_text="Presença de insuficiência renal")
    hepatite = models.BooleanField(default=False, help_text="Presença de hepatite")
    
    # Controle de análise KalaCal
    kalacal_habilitado = models.BooleanField(
        default=False, 
        help_text="Indica se este caso está habilitado para análise KalaCal"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Caso'
        verbose_name_plural = 'Casos'
        ordering = ['-data_notificacao']
    
    def __str__(self):
        tipo = "Paciente" if self.tipo_caso == 'humano' else "Animal"
        return f"{self.identificador} - {tipo} - {self.data_notificacao}"
    
    def is_crianca_kalacal(self):
        """Verifica se é criança para análise KalaCal (< 2 anos)"""
        if self.faixa_etaria_kalacal:
            return self.faixa_etaria_kalacal in [FaixaEtaria.MENOR_12M, FaixaEtaria.ENTRE_12_23M]
        return False
    
    def is_adulto_kalacal(self):
        """Verifica se é adulto para análise KalaCal (>= 2 anos)"""
        return not self.is_crianca_kalacal()
    
    def calcular_faixa_etaria_automatica(self):
        """Calcula a faixa etária baseada na data de nascimento"""
        if not self.data_nascimento:
            return None
        
        hoje = date.today()
        idade_anos = hoje.year - self.data_nascimento.year
        idade_meses = (hoje.year - self.data_nascimento.year) * 12 + hoje.month - self.data_nascimento.month
        
        if idade_meses < 12:
            return FaixaEtaria.MENOR_12M
        elif idade_meses < 24:
            return FaixaEtaria.ENTRE_12_23M
        elif idade_anos <= 15:
            return FaixaEtaria.ENTRE_2_15A
        elif idade_anos <= 40:
            return FaixaEtaria.ENTRE_16_40A
        else:
            return FaixaEtaria.MAIOR_40A
    
    def get_dados_kalacal(self):
        """Retorna dados formatados para cálculo KalaCal"""
        return {
            'faixa_etaria': self.faixa_etaria_kalacal or self.calcular_faixa_etaria_automatica(),
            'sitios_sangramento': self.sitios_sangramento or SitiosSangramento.NENHUM,
            'edema': self.edema,
            'aids': self.aids,
            'ictericia': self.ictericia,
            'dispneia': self.dispneia,
            'infeccao': self.infeccao,
            'vomitos': self.vomitos,
            'leucopenia': self.leucopenia,
            'plaquetopenia': self.plaquetopenia,
            'insuficiencia_renal': self.insuficiencia_renal,
            'hepatite': self.hepatite,
        }
