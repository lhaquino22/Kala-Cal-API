from rest_framework import serializers
from .models import Caso, FaixaEtaria, SitiosSangramento

class CasoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_caso_display', read_only=True)
    faixa_etaria_kalacal_display = serializers.CharField(source='get_faixa_etaria_kalacal_display', read_only=True)
    sitios_sangramento_display = serializers.CharField(source='get_sitios_sangramento_display', read_only=True)
    is_crianca_kalacal = serializers.BooleanField(read_only=True)
    is_adulto_kalacal = serializers.BooleanField(read_only=True)
    faixa_etaria_automatica = serializers.SerializerMethodField()
    
    class Meta:
        model = Caso
        fields = [
            'id', 'identificador', 'tipo_caso', 'tipo_display',
            'data_nascimento', 'sexo', 'gestante', 'data_notificacao',
            'latitude', 'longitude', 'municipio', 'created_at', 'updated_at',
            
            'faixa_etaria_kalacal', 'faixa_etaria_kalacal_display',
            'sitios_sangramento', 'sitios_sangramento_display',
            'edema', 'aids', 'ictericia', 'dispneia', 'infeccao', 'vomitos',
            'leucopenia', 'plaquetopenia', 'insuficiencia_renal', 'hepatite',
            'kalacal_habilitado',
            
            'is_crianca_kalacal', 'is_adulto_kalacal', 'faixa_etaria_automatica'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_faixa_etaria_automatica(self, obj):
        """Retorna a faixa etária calculada automaticamente baseada na data de nascimento"""
        faixa = obj.calcular_faixa_etaria_automatica()
        if faixa:
            return {
                'value': faixa,
                'label': FaixaEtaria(faixa).label
            }
        return None

class CasoKalaCalSerializer(serializers.ModelSerializer):
    """Serializer específico para operações KalaCal"""
    tipo_display = serializers.CharField(source='get_tipo_caso_display', read_only=True)
    faixa_etaria_kalacal_display = serializers.CharField(source='get_faixa_etaria_kalacal_display', read_only=True)
    sitios_sangramento_display = serializers.CharField(source='get_sitios_sangramento_display', read_only=True)
    dados_kalacal = serializers.SerializerMethodField()
    
    class Meta:
        model = Caso
        fields = [
            'id', 'identificador', 'tipo_display',
            'faixa_etaria_kalacal', 'faixa_etaria_kalacal_display',
            'sitios_sangramento', 'sitios_sangramento_display',
            'edema', 'aids', 'ictericia', 'dispneia', 'infeccao', 'vomitos',
            'leucopenia', 'plaquetopenia', 'insuficiencia_renal', 'hepatite',
            'kalacal_habilitado', 'dados_kalacal'
        ]
    
    def get_dados_kalacal(self, obj):
        """Retorna os dados formatados para cálculo KalaCal"""
        return obj.get_dados_kalacal()

class CasoKalaCalRequestSerializer(serializers.Serializer):
    """Serializer para requisições de cálculo KalaCal em casos existentes"""
    caso_id = serializers.IntegerField()
    modelo = serializers.ChoiceField(choices=[('clinico', 'Clínico'), ('clinico_laboratorial', 'Clínico e Laboratorial')])
    
    # Campos opcionais para atualizar dados do caso antes do cálculo
    faixa_etaria_kalacal = serializers.ChoiceField(choices=FaixaEtaria.choices, required=False)
    sitios_sangramento = serializers.ChoiceField(choices=SitiosSangramento.choices, required=False)
    edema = serializers.BooleanField(required=False)
    aids = serializers.BooleanField(required=False)
    ictericia = serializers.BooleanField(required=False)
    dispneia = serializers.BooleanField(required=False)
    infeccao = serializers.BooleanField(required=False)
    vomitos = serializers.BooleanField(required=False)
    leucopenia = serializers.BooleanField(required=False)
    plaquetopenia = serializers.BooleanField(required=False)
    insuficiencia_renal = serializers.BooleanField(required=False)
    hepatite = serializers.BooleanField(required=False)
    observacoes = serializers.CharField(max_length=500, required=False, allow_blank=True) 