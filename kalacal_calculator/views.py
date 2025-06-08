from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import CalculoKalaCal
from casos.models import Caso, FaixaEtaria, SitiosSangramento
from casos.serializers import CasoSerializer
from .serializers import (
    CalculoKalaCalSerializer,
    CalculoRequestSerializer,
    CalculoResponseSerializer,
    MetricasKalaCalSerializer,
    OpcoesFormularioSerializer
)
from .services import KalaCalService

class CasosComCalculosListView(generics.ListAPIView):
    """Lista casos que possuem cálculos KalaCal"""
    serializer_class = CasoSerializer
    
    def get_queryset(self):
        # Retorna casos que têm pelo menos um cálculo
        return Caso.objects.filter(calculos_kalacal__isnull=False).distinct().order_by('-created_at')

class CalculoKalaCalListView(generics.ListAPIView):
    """Lista cálculos realizados"""
    queryset = CalculoKalaCal.objects.all()
    serializer_class = CalculoKalaCalSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros opcionais
        modelo = self.request.query_params.get('modelo')
        if modelo:
            queryset = queryset.filter(modelo_usado=modelo)
        
        caso_id = self.request.query_params.get('caso_id')
        if caso_id:
            queryset = queryset.filter(caso_id=caso_id)
            
        return queryset.order_by('-calculado_em')

@api_view(['POST'])
def calcular_probabilidade(request):
    """
    Calcula probabilidade de morte para um caso específico.
    Automaticamente salva o histórico de cálculos.
    """
    serializer = CalculoRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    dados = serializer.validated_data
    caso_id = dados.pop('caso_id')
    modelo = dados.pop('modelo')
    observacoes = dados.pop('observacoes', '')
    
    try:
        # Buscar o caso (pode usar ID ou identificador)
        # Tenta primeiro como ID numérico, depois como identificador
        if str(caso_id).isdigit():
            caso = get_object_or_404(Caso, id=int(caso_id))
        else:
            caso = get_object_or_404(Caso, identificador=caso_id)
        
        # Atualizar dados do caso se fornecidos na requisição
        campos_para_atualizar = {}
        for campo in ['faixa_etaria_kalacal', 'sitios_sangramento', 'edema', 'aids', 
                     'ictericia', 'dispneia', 'infeccao', 'vomitos', 'leucopenia', 
                     'plaquetopenia', 'insuficiencia_renal', 'hepatite']:
            if campo in dados:
                campos_para_atualizar[campo] = dados[campo]
        
        if campos_para_atualizar:
            for campo, valor in campos_para_atualizar.items():
                setattr(caso, campo, valor)
            caso.save()
        
        # Obter dados para cálculo
        dados_calculo = caso.get_dados_kalacal()
        
        # Verificar se temos dados suficientes
        if not dados_calculo.get('faixa_etaria'):
            return Response(
                {'error': 'Faixa etária é obrigatória. Defina faixa_etaria_kalacal ou data_nascimento no caso.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcular escore e probabilidade
        escore, probabilidade_morte = KalaCalService.calcular_probabilidade(dados_calculo, modelo)
        
        # Determinar escore máximo baseado na faixa etária e modelo
        is_crianca = caso.is_crianca_kalacal()
        if is_crianca:
            escore_maximo = 11 if modelo == 'clinico_laboratorial' else 9
        else:
            escore_maximo = 13 if modelo == 'clinico' else 10
        
        # Criar registro do cálculo (salva automaticamente no histórico)
        calculo = CalculoKalaCal.objects.create(
            caso=caso,
            modelo_usado=modelo,
            escore=escore,
            probabilidade_morte=probabilidade_morte,
            observacoes=observacoes
        )
        
        # Preparar resposta simples sem serializer complexo
        response_data = {
            'caso_id': caso.id,
            'escore': escore,
            'escore_maximo': escore_maximo,
            'probabilidade_morte': probabilidade_morte,
            'modelo_usado': modelo,
            'interpretacao': calculo.get_interpretacao(),
            'calculo_id': calculo.id,
            'calculado_em': calculo.calculado_em
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Caso.DoesNotExist:
        return Response(
            {'error': 'Caso não encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Erro no cálculo: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def opcoes_formulario(request):
    """
    Retorna as opções disponíveis para os formulários
    """
    response_data = {
        'faixas_etarias': [
            {'value': key, 'label': value} 
            for key, value in FaixaEtaria.choices
        ],
        'sitios_sangramento': [
            {'value': key, 'label': value} 
            for key, value in SitiosSangramento.choices
        ],
        'modelos': [
            {'value': key, 'label': value} 
            for key, value in CalculoKalaCal.MODELO_CHOICES
        ],
        'sinais_clinicos': [
            {'key': 'edema', 'label': 'Edema'},
            {'key': 'aids', 'label': 'AIDS'},
            {'key': 'ictericia', 'label': 'Icterícia'},
            {'key': 'dispneia', 'label': 'Dispneia'},
            {'key': 'infeccao', 'label': 'Infecção'},
            {'key': 'vomitos', 'label': 'Vômitos'},
        ],
        'dados_laboratoriais': [
            {'key': 'leucopenia', 'label': 'Leucopenia'},
            {'key': 'plaquetopenia', 'label': 'Plaquetopenia'},
            {'key': 'insuficiencia_renal', 'label': 'Insuficiência Renal'},
            {'key': 'hepatite', 'label': 'Hepatite'},
        ]
    }
    
    serializer = OpcoesFormularioSerializer(response_data)
    return Response(serializer.data)

@api_view(['GET'])
def metricas_sistema(request):
    """
    Retorna métricas e estatísticas do sistema
    """
    try:
        # Estatísticas gerais
        total_calculos = CalculoKalaCal.objects.count()
        total_casos_com_calculos = Caso.objects.filter(calculos_kalacal__isnull=False).distinct().count()
        
        # Cálculos por modelo
        calculos_por_modelo = dict(
            CalculoKalaCal.objects.values('modelo_usado')
            .annotate(count=Count('id'))
            .values_list('modelo_usado', 'count')
        )
        
        # Cálculos por faixa etária
        calculos_por_faixa = dict(
            CalculoKalaCal.objects.values('caso__faixa_etaria_kalacal')
            .annotate(count=Count('id'))
            .values_list('caso__faixa_etaria_kalacal', 'count')
        )
        
        # Média de probabilidade por modelo
        media_prob_modelo = {}
        for modelo, _ in CalculoKalaCal.MODELO_CHOICES:
            avg = CalculoKalaCal.objects.filter(modelo_usado=modelo).aggregate(
                media=Avg('probabilidade_morte')
            )['media']
            media_prob_modelo[modelo] = round(avg, 2) if avg else 0.0
        
        # Distribuição de escores
        distribuicao_escores = dict(
            CalculoKalaCal.objects.values('escore')
            .annotate(count=Count('id'))
            .values_list('escore', 'count')
        )
        
        # Casos por interpretação
        casos_por_interpretacao = {}
        for calculo in CalculoKalaCal.objects.all():
            interpretacao = calculo.get_interpretacao()
            casos_por_interpretacao[interpretacao] = casos_por_interpretacao.get(interpretacao, 0) + 1
        
        response_data = {
            'total_calculos': total_calculos,
            'total_casos_com_calculos': total_casos_com_calculos,
            'calculos_por_modelo': calculos_por_modelo,
            'calculos_por_faixa_etaria': calculos_por_faixa,
            'media_probabilidade': media_prob_modelo,
            'distribuicao_escores': distribuicao_escores,
            'casos_por_interpretacao': casos_por_interpretacao
        }
        
        serializer = MetricasKalaCalSerializer(response_data)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': f'Erro ao obter métricas: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def historico_caso(request, caso_id):
    """
    Retorna histórico de cálculos de um caso específico
    """
    try:
        # Aceita ID numérico ou identificador string
        if caso_id.isdigit():
            caso = get_object_or_404(Caso, id=caso_id)
        else:
            caso = get_object_or_404(Caso, identificador=caso_id)
        
        calculos = CalculoKalaCal.objects.filter(caso=caso).order_by('-calculado_em')
        
        # Import local para evitar problemas circulares
        from casos.serializers import CasoKalaCalSerializer
        caso_serializer = CasoKalaCalSerializer(caso)
        calculos_serializer = CalculoKalaCalSerializer(calculos, many=True)
        
        return Response({
            'caso': caso_serializer.data,
            'historico_calculos': calculos_serializer.data,
            'total_calculos': calculos.count()
        })
        
    except Caso.DoesNotExist:
        return Response(
            {'error': 'Caso não encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )

def _get_interpretacao(probabilidade: float) -> str:
    """
    Retorna interpretação textual da probabilidade de morte
    """
    if probabilidade < 5:
        return "Risco baixo"
    elif probabilidade < 20:
        return "Risco moderado"
    elif probabilidade < 50:
        return "Risco alto"
    else:
        return "Risco muito alto"
