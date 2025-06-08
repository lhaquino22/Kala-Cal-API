from django.contrib import admin
from .models import CalculoKalaCal

@admin.register(CalculoKalaCal)
class CalculoKalaCalAdmin(admin.ModelAdmin):
    list_display = [
        'caso', 'modelo_usado', 'escore', 'probabilidade_morte', 
        'get_interpretacao', 'calculado_em'
    ]
    list_filter = ['modelo_usado', 'escore', 'calculado_em']
    search_fields = ['caso__identificador', 'caso__municipio']
    ordering = ['-calculado_em']
    readonly_fields = ['calculado_em']
    
    fieldsets = (
        ('Caso', {
            'fields': ('caso',)
        }),
        ('Cálculo', {
            'fields': ('modelo_usado', 'escore', 'probabilidade_morte')
        }),
        ('Detalhes', {
            'fields': ('observacoes', 'calculado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_interpretacao(self, obj):
        """Retorna interpretação do risco"""
        return obj.get_interpretacao()
    get_interpretacao.short_description = 'Interpretação'
    get_interpretacao.admin_order_field = 'probabilidade_morte'
