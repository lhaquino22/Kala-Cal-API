from django.urls import path
from . import views

urlpatterns = [
    # Endpoint principal
    path('calcular/', views.calcular_probabilidade, name='calcular_probabilidade'),
    
    # Informações e métricas
    path('opcoes/', views.opcoes_formulario, name='opcoes_formulario'),
    path('metricas/', views.metricas_sistema, name='metricas_sistema'),
    
    # Casos com cálculos
    path('casos/', views.CasosComCalculosListView.as_view(), name='casos_com_calculos_list'),
    path('casos/<str:caso_id>/historico/', views.historico_caso, name='historico_caso'),
    
    # Histórico de cálculos
    path('calculos/', views.CalculoKalaCalListView.as_view(), name='calculos_list'),
] 