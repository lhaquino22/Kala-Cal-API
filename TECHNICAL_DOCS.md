# Documentação Técnica - Sistema KalaKal

## Visão Geral da Arquitetura

### Estrutura do Projeto
```
kalacal_backend/
├── kalacal_backend/           # Configurações Django
│   ├── settings.py           # Configurações principais
│   ├── urls.py              # URLs raiz
│   └── wsgi.py              # WSGI configuration
├── casos/                   # App de gerenciamento de casos
│   ├── models.py           # Modelo Caso
│   ├── serializers.py      # Serializers DRF
│   ├── views.py            # ViewSets
│   ├── admin.py            # Interface admin
│   └── migrations/         # Migrações de BD
├── kalacal_calculator/      # App de cálculos epidemiológicos
│   ├── models.py           # Modelo CalculoKalaCal
│   ├── serializers.py      # Serializers específicos
│   ├── views.py            # Views de cálculo
│   ├── services.py         # Lógica de negócio
│   ├── admin.py            # Admin customizado
│   └── management/         # Comandos customizados
└── requirements.txt        # Dependências
```

## Modelos de Dados

### Caso (casos/models.py)

```python
class Caso(models.Model):
    # === IDENTIFICAÇÃO ===
    identificador = models.CharField(max_length=50, unique=True)
    tipo_caso = models.CharField(max_length=10, choices=TipoCaso.choices)
    
    # === DADOS PESSOAIS ===
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=Sexo.choices)
    gestante = models.BooleanField(default=False, null=True, blank=True)
    
    # === NOTIFICAÇÃO ===
    data_notificacao = models.DateField(default=date.today)
    
    # === LOCALIZAÇÃO ===
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    municipio = models.CharField(max_length=100, blank=True)
    
    # === CAMPOS KALACAL ===
    faixa_etaria_kalacal = models.IntegerField(choices=FaixaEtaria.choices, null=True, blank=True)
    sitios_sangramento = models.IntegerField(choices=SitiosSangramento.choices, null=True, blank=True)
    
    # Sinais clínicos (Boolean fields)
    edema = models.BooleanField(default=False)
    aids = models.BooleanField(default=False)
    ictericia = models.BooleanField(default=False)
    dispneia = models.BooleanField(default=False)
    infeccao = models.BooleanField(default=False)
    vomitos = models.BooleanField(default=False)
    
    # Dados laboratoriais (Boolean fields)
    leucopenia = models.BooleanField(default=False)
    plaquetopenia = models.BooleanField(default=False)
    insuficiencia_renal = models.BooleanField(default=False)
    hepatite = models.BooleanField(default=False)
    
    # Controle
    kalacal_habilitado = models.BooleanField(default=False)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### CalculoKalaCal (kalacal_calculator/models.py)

```python
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
    observacoes = models.TextField(blank=True)
```

## Serviços de Negócio

### KalaCalService (kalacal_calculator/services.py)

Implementa os algoritmos epidemiológicos originais.

#### Principais Métodos:

```python
class KalaCalService:
    @staticmethod
    def calcular_probabilidade(dados: dict, modelo: str) -> Tuple[int, float]:
        """Método principal de cálculo"""
        
    @staticmethod
    def calcular_escore_clinico_crianca(dados: dict) -> int:
        """Escore clínico para < 2 anos"""
        
    @staticmethod
    def calcular_escore_laboratorial_crianca(dados: dict) -> int:
        """Escore clínico+laboratorial para < 2 anos"""
        
    @staticmethod
    def calcular_escore_clinico_adulto(dados: dict) -> int:
        """Escore clínico para >= 2 anos"""
        
    @staticmethod
    def calcular_escore_laboratorial_adulto(dados: dict) -> int:
        """Escore clínico+laboratorial para >= 2 anos"""
```

#### Algoritmos de Probabilidade:

```python
# Exemplo do método para adultos - modelo clínico
@staticmethod
def prob_morte_maior_2anos_clinico(escore: int) -> float:
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
        10: 0.907745889,
        11: 0.955925539,
        12: 0.979297619,
        13: 0.9901837219,
    }
    return KalaCalService.limitar_casas_decimais(probabilidades.get(escore, 0.0))
```

## Views e Endpoints

### Casos (casos/views.py)

```python
class CasoViewSet(viewsets.ModelViewSet):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['identificador', 'municipio']
    filterset_fields = ['tipo_caso', 'sexo', 'data_notificacao', 'kalacal_habilitado']
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """Endpoint customizado para estatísticas por tipo"""
```

### KalaCal Calculator (kalacal_calculator/views.py)

```python
@api_view(['POST'])
def calcular_probabilidade(request):
    """Endpoint principal de cálculo"""
    # 1. Validar dados de entrada
    # 2. Buscar caso (ID ou identificador)
    # 3. Atualizar caso se necessário
    # 4. Executar cálculo
    # 5. Salvar histórico
    # 6. Retornar resposta

@api_view(['GET'])
def opcoes_formulario(request):
    """Retorna opções para formulários dinâmicos"""

@api_view(['GET'])
def metricas_sistema(request):
    """Estatísticas e métricas do sistema"""

@api_view(['GET'])
def historico_caso(request, caso_id):
    """Histórico de cálculos de um caso"""
```

## Serializers

### CasoSerializer (casos/serializers.py)

```python
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
            # Campos básicos
            'id', 'identificador', 'tipo_caso', 'tipo_display',
            'data_nascimento', 'sexo', 'gestante', 'data_notificacao',
            'latitude', 'longitude', 'municipio', 'created_at', 'updated_at',
            
            # Campos KalaCal
            'faixa_etaria_kalacal', 'faixa_etaria_kalacal_display',
            'sitios_sangramento', 'sitios_sangramento_display',
            'edema', 'aids', 'ictericia', 'dispneia', 'infeccao', 'vomitos',
            'leucopenia', 'plaquetopenia', 'insuficiencia_renal', 'hepatite',
            'kalacal_habilitado',
            
            # Campos calculados
            'is_crianca_kalacal', 'is_adulto_kalacal', 'faixa_etaria_automatica'
        ]
```

### CalculoRequestSerializer (kalacal_calculator/serializers.py)

```python
class CalculoRequestSerializer(serializers.Serializer):
    caso_id = serializers.CharField(help_text="ID numérico ou identificador do caso")
    modelo = serializers.ChoiceField(choices=CalculoKalaCal.MODELO_CHOICES)
    
    # Campos opcionais para atualizar o caso
    faixa_etaria_kalacal = serializers.ChoiceField(choices=FaixaEtaria.choices, required=False)
    sitios_sangramento = serializers.ChoiceField(choices=SitiosSangramento.choices, required=False)
    
    # Sinais clínicos (opcionais)
    edema = serializers.BooleanField(required=False)
    aids = serializers.BooleanField(required=False)
    # ... outros campos
    
    def validate_caso_id(self, value):
        """Validação customizada para aceitar ID ou identificador"""
        if value.isdigit():
            if not Caso.objects.filter(id=value).exists():
                raise serializers.ValidationError("Caso com este ID não encontrado.")
        else:
            if not Caso.objects.filter(identificador=value).exists():
                raise serializers.ValidationError("Caso com este identificador não encontrado.")
        return value
```

## Configurações

### settings.py

```python
# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'casos',
    'kalacal_calculator',
]

# CORS configuração
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",  # Expo dev server
    "http://10.0.2.2:8000",  # Android emulator
]
CORS_ALLOW_ALL_ORIGINS = True  # Para desenvolvimento

# DRF configuração
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}
```

### URLs Principais

```python
# kalacal_backend/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('casos.urls')),
    path('api/kalacal/', include('kalacal_calculator.urls')),
]

# casos/urls.py
router = DefaultRouter()
router.register(r'casos', CasoViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
]

# kalacal_calculator/urls.py
urlpatterns = [
    path('calcular/', views.calcular_probabilidade, name='calcular_probabilidade'),
    path('opcoes/', views.opcoes_formulario, name='opcoes_formulario'),
    path('metricas/', views.metricas_sistema, name='metricas_sistema'),
    path('casos/', views.CasosComCalculosListView.as_view(), name='casos_com_calculos_list'),
    path('casos/<str:caso_id>/historico/', views.historico_caso, name='historico_caso'),
    path('calculos/', views.CalculoKalaCalListView.as_view(), name='calculos_list'),
]
```

## Comandos de Gerenciamento

### populate_casos.py

```python
from django.core.management.base import BaseCommand
from casos.models import Caso

class Command(BaseCommand):
    help = 'Popula o banco de dados com casos de exemplo'
    
    def handle(self, *args, **options):
        # Criar casos de exemplo
        casos_exemplo = [
            {
                'identificador': 'H001',
                'tipo_caso': 'humano',
                'sexo': 'masculino',
                # ... outros campos
            },
            # ... mais casos
        ]
        
        for dados_caso in casos_exemplo:
            caso, created = Caso.objects.get_or_create(
                identificador=dados_caso['identificador'],
                defaults=dados_caso
            )
            if created:
                self.stdout.write(f'Criado: {caso.identificador}')
```

### populate_kalacal.py

```python
from django.core.management.base import BaseCommand
from casos.models import Caso, FaixaEtaria, SitiosSangramento
from kalacal_calculator.models import CalculoKalaCal
from kalacal_calculator.services import KalaCalService

class Command(BaseCommand):
    help = 'Popula o banco com casos KalaCal e faz cálculos de exemplo'
    
    def handle(self, *args, **options):
        # Criar casos específicos para KalaCal
        # Executar cálculos de exemplo
        # Gerar histórico de dados
```

## Interface Administrativa

### Caso Admin (casos/admin.py)

```python
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
        ('Análise KalaCal', {
            'fields': (
                'kalacal_habilitado',
                'faixa_etaria_kalacal',
                'sitios_sangramento',
            ),
            'classes': ('collapse',)
        }),
        # ... outros fieldsets
    )
    
    actions = ['habilitar_kalacal', 'desabilitar_kalacal']
    
    def habilitar_kalacal(self, request, queryset):
        updated = queryset.update(kalacal_habilitado=True)
        self.message_user(request, f'{updated} casos habilitados para KalaCal.')
```

### CalculoKalaCal Admin (kalacal_calculator/admin.py)

```python
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
    
    def get_interpretacao(self, obj):
        return obj.get_interpretacao()
    get_interpretacao.short_description = 'Interpretação'
```

## Testes e Validação

### Estrutura de Testes

```python
# tests/test_models.py
class CasoModelTest(TestCase):
    def test_calculo_faixa_etaria_automatica(self):
        """Testa cálculo automático de faixa etária"""
        
    def test_is_crianca_kalacal(self):
        """Testa classificação criança/adulto"""

# tests/test_services.py  
class KalaCalServiceTest(TestCase):
    def test_calculo_escore_crianca_clinico(self):
        """Testa cálculo de escore para criança - modelo clínico"""
        
    def test_calculo_probabilidade_adulto_laboratorial(self):
        """Testa cálculo completo para adulto - modelo laboratorial"""

# tests/test_views.py
class CalculoViewTest(APITestCase):
    def test_calcular_probabilidade_sucesso(self):
        """Testa endpoint de cálculo com dados válidos"""
        
    def test_calcular_probabilidade_caso_inexistente(self):
        """Testa endpoint com caso inexistente"""
```

### Comando de Teste

```bash
# Executar todos os testes
python manage.py test

# Testes específicos
python manage.py test casos.tests.test_models
python manage.py test kalacal_calculator.tests.test_services

# Testes com coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Performance e Otimização

### Queries Otimizadas

```python
# Evitar N+1 queries
class CasosComCalculosListView(generics.ListAPIView):
    def get_queryset(self):
        return Caso.objects.filter(
            calculos_kalacal__isnull=False
        ).distinct().select_related().prefetch_related('calculos_kalacal')

# Uso de select_related para ForeignKeys
calculos = CalculoKalaCal.objects.select_related('caso').all()

# Uso de prefetch_related para relacionamentosMany-to-Many
casos = Caso.objects.prefetch_related('calculos_kalacal').all()
```

### Caching

```python
# Cache de opções estáticas
from django.core.cache import cache

def opcoes_formulario(request):
    cache_key = 'kalacal_opcoes_formulario'
    opcoes = cache.get(cache_key)
    
    if opcoes is None:
        opcoes = {
            'faixas_etarias': [{'value': k, 'label': v} for k, v in FaixaEtaria.choices],
            # ... outras opções
        }
        cache.set(cache_key, opcoes, 3600)  # Cache por 1 hora
    
    return Response(opcoes)
```

## Segurança

### Validações

```python
# Validação de dados de entrada
def validate_caso_id(self, value):
    if not value or len(str(value).strip()) == 0:
        raise serializers.ValidationError("caso_id é obrigatório")
    return value

# Sanitização de parâmetros
def get_queryset(self):
    queryset = super().get_queryset()
    modelo = self.request.query_params.get('modelo')
    if modelo and modelo in ['clinico', 'clinico_laboratorial']:
        queryset = queryset.filter(modelo_usado=modelo)
    return queryset
```

### Permissions (para futuras versões)

```python
from rest_framework.permissions import IsAuthenticated

class CasoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Requerer autenticação
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
```

## Deployment

### Requirements.txt

```txt
Django==5.2.2
djangorestframework==3.15.1
django-cors-headers==4.3.1
django-filter==24.2
psycopg2-binary==2.9.7  # Para PostgreSQL
python-decouple==3.8   # Para variáveis de ambiente
gunicorn==21.2.0       # Para produção
```

### Configurações de Produção

```python
# settings/production.py
import os
from decouple import config

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])

# Database PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Security
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kalacal_backend.wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DB_NAME=kalacal_db
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: kalacal_db
      POSTGRES_USER: kalacal_user
      POSTGRES_PASSWORD: kalacal_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Monitoramento e Logs

### Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'kalacal.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'kalacal_calculator': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Uso em views
import logging
logger = logging.getLogger('kalacal_calculator')

def calcular_probabilidade(request):
    logger.info(f"Iniciando cálculo para caso: {request.data.get('caso_id')}")
    # ... lógica
    logger.info(f"Cálculo concluído: escore={escore}, prob={probabilidade}")
```

---

*Documentação técnica atualizada em Junho 2025*
*Sistema desenvolvido com Django 5.2.2 + Django REST Framework* 