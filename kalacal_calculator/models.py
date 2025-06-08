from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from casos.models import Caso

class CalculoKalaCal(models.Model):
    MODELO_CHOICES = [
        ('clinico', 'Clínico'),
        ('clinico_laboratorial', 'Clínico e Laboratorial'),
    ]
    
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='calculos_kalacal')
    modelo_usado = models.CharField(max_length=30, choices=MODELO_CHOICES)
    
    # Resultados
    escore = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(13)])
    probabilidade_morte = models.FloatField(help_text="Probabilidade de morte em %")
    
    # Metadados
    calculado_em = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, help_text="Observações adicionais sobre o cálculo")
    
    class Meta:
        verbose_name = "Cálculo KalaCal"
        verbose_name_plural = "Cálculos KalaCal"
        ordering = ['-calculado_em']
    
    def __str__(self):
        return f"{self.caso.identificador} - {self.modelo_usado} - {self.probabilidade_morte}%"
    
    def get_interpretacao(self):
        """Retorna interpretação textual da probabilidade de morte"""
        if self.probabilidade_morte < 5:
            return "Risco baixo"
        elif self.probabilidade_morte < 20:
            return "Risco moderado"
        elif self.probabilidade_morte < 50:
            return "Risco alto"
        else:
            return "Risco muito alto"
