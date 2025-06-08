from rest_framework import serializers
from .models import CalculoKalaCal
from casos.models import Caso, FaixaEtaria, SitiosSangramento
from .services import KalaCalService

class CalculoKalaCalSerializer(serializers.ModelSerializer):
    # Removendo referência circular - vamos usar apenas campos básicos do caso
    caso_identificador = serializers.CharField(source='caso.identificador', read_only=True)
    caso_municipio = serializers.CharField(source='caso.municipio', read_only=True)
    modelo_usado_display = serializers.CharField(source='get_modelo_usado_display', read_only=True)
    interpretacao = serializers.CharField(source='get_interpretacao', read_only=True)
    
    class Meta:
        model = CalculoKalaCal
        fields = ['id', 'caso_identificador', 'caso_municipio', 'modelo_usado', 'modelo_usado_display', 
                 'escore', 'probabilidade_morte', 'interpretacao', 'calculado_em', 'observacoes']
        read_only_fields = ['calculado_em']

class CalculoRequestSerializer(serializers.Serializer):
    """Serializer para requisições de cálculo de probabilidade"""
    # Aceita tanto ID numérico quanto identificador string
    caso_id = serializers.CharField(help_text="ID numérico ou identificador do caso")
    modelo = serializers.ChoiceField(choices=CalculoKalaCal.MODELO_CHOICES)
    
    # Campos opcionais para atualizar o caso antes do cálculo
    faixa_etaria_kalacal = serializers.ChoiceField(choices=FaixaEtaria.choices, required=False)
    sitios_sangramento = serializers.ChoiceField(choices=SitiosSangramento.choices, required=False)
    
    # Dados opcionais (sinais clínicos)
    edema = serializers.BooleanField(required=False)
    aids = serializers.BooleanField(required=False)
    ictericia = serializers.BooleanField(required=False)
    dispneia = serializers.BooleanField(required=False)
    infeccao = serializers.BooleanField(required=False)
    vomitos = serializers.BooleanField(required=False)
    
    # Dados laboratoriais (opcionais)
    leucopenia = serializers.BooleanField(required=False)
    plaquetopenia = serializers.BooleanField(required=False)
    insuficiencia_renal = serializers.BooleanField(required=False)
    hepatite = serializers.BooleanField(required=False)
    
    # Observações
    observacoes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_caso_id(self, value):
        """Valida se o caso existe (por ID ou identificador)"""
        if value.isdigit():
            # É um ID numérico
            if not Caso.objects.filter(id=value).exists():
                raise serializers.ValidationError("Caso com este ID não encontrado.")
        else:
            # É um identificador string
            if not Caso.objects.filter(identificador=value).exists():
                raise serializers.ValidationError("Caso com este identificador não encontrado.")
        return value

class CalculoResponseSerializer(serializers.Serializer):
    """Serializer para resposta do cálculo de probabilidade"""
    caso_id = serializers.IntegerField()
    escore = serializers.IntegerField()
    escore_maximo = serializers.IntegerField()
    probabilidade_morte = serializers.FloatField()
    modelo_usado = serializers.CharField()
    interpretacao = serializers.CharField()
    calculo_id = serializers.IntegerField()
    calculado_em = serializers.DateTimeField()

class MetricasKalaCalSerializer(serializers.Serializer):
    """Serializer para métricas e estatísticas do sistema"""
    total_calculos = serializers.IntegerField()
    total_casos_com_calculos = serializers.IntegerField()
    calculos_por_modelo = serializers.DictField()
    calculos_por_faixa_etaria = serializers.DictField()
    media_probabilidade = serializers.DictField()
    distribuicao_escores = serializers.DictField()
    casos_por_interpretacao = serializers.DictField()

class OpcoesFormularioSerializer(serializers.Serializer):
    """Serializer para opções dos formulários"""
    faixas_etarias = serializers.ListField()
    sitios_sangramento = serializers.ListField()
    modelos = serializers.ListField()
    sinais_clinicos = serializers.ListField()
    dados_laboratoriais = serializers.ListField() 