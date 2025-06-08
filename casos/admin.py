from django.contrib import admin
from .models import Caso

@admin.register(Caso)
class CasoAdmin(admin.ModelAdmin):
    list_display = [
        'identificador', 'tipo_caso', 'sexo', 'data_notificacao', 
        'municipio', 'kalacal_habilitado', 'get_faixa_etaria_kalacal_display'
    ]
    list_filter = [
        'tipo_caso', 'sexo', 'data_notificacao', 'kalacal_habilitado',
        'faixa_etaria_kalacal', 'sitios_sangramento', 'edema', 'aids'
    ]
    search_fields = ['identificador', 'municipio']
    date_hierarchy = 'data_notificacao'
    
    fieldsets = (
        ('Identificação', {
            'fields': ('identificador', 'tipo_caso')
        }),
        ('Dados Pessoais', {
            'fields': ('data_nascimento', 'sexo', 'gestante')
        }),
        ('Notificação', {
            'fields': ('data_notificacao',)
        }),
        ('Localização', {
            'fields': ('municipio', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Análise KalaCal', {
            'fields': (
                'kalacal_habilitado',
                'faixa_etaria_kalacal',
                'sitios_sangramento',
            ),
            'classes': ('collapse',)
        }),
        ('Sinais Clínicos', {
            'fields': (
                'edema', 'aids', 'ictericia', 'dispneia', 'infeccao', 'vomitos'
            ),
            'classes': ('collapse',)
        }),
        ('Dados Laboratoriais', {
            'fields': (
                'leucopenia', 'plaquetopenia', 'insuficiencia_renal', 'hepatite'
            ),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['habilitar_kalacal', 'desabilitar_kalacal']
    
    def habilitar_kalacal(self, request, queryset):
        """Habilita casos selecionados para análise KalaCal"""
        updated = queryset.update(kalacal_habilitado=True)
        self.message_user(request, f'{updated} casos habilitados para análise KalaCal.')
    habilitar_kalacal.short_description = "Habilitar para análise KalaCal"
    
    def desabilitar_kalacal(self, request, queryset):
        """Desabilita casos selecionados para análise KalaCal"""
        updated = queryset.update(kalacal_habilitado=False)
        self.message_user(request, f'{updated} casos desabilitados para análise KalaCal.')
    desabilitar_kalacal.short_description = "Desabilitar análise KalaCal"
