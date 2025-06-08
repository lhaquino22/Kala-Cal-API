from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Caso
from .serializers import CasoSerializer

# Create your views here.

class CasoViewSet(viewsets.ModelViewSet):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tipo_caso', 'sexo', 'data_notificacao']
    search_fields = ['identificador', 'municipio']
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        humanos = self.queryset.filter(tipo_caso='humano').count()
        animais = self.queryset.filter(tipo_caso='animal').count()
        return Response({
            'humanos': humanos,
            'animais': animais,
            'total': humanos + animais
        })
