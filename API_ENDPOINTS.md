# Documentação Completa da API KalaKal

## Sumário Executivo

O sistema KalaKal é uma API Django REST que implementa algoritmos epidemiológicos para cálculo de probabilidade de morte em pacientes com Kala-azar, baseado em dados de Teresina-PI (2005-2013). O sistema foi desenvolvido transformando código PHP original em uma arquitetura moderna de microsserviços.

## Arquitetura do Sistema

### Aplicações Django

1. **`casos`** - Gerenciamento de casos (pacientes/animais)
2. **`kalacal_calculator`** - Sistema de cálculos epidemiológicos

### URLs Base
- **Desenvolvimento Local**: `http://localhost:8000`
- **Para Emulador Android**: `http://10.0.2.2:8000`
- **Para Dispositivo Físico**: `http://SEU_IP_LOCAL:8000`

---

## 📊 APLICAÇÃO CASOS

### Modelo Principal: `Caso`

Representa pacientes humanos ou animais com potencial Kala-azar.

#### Campos Base
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `identificador` | String(50) | ✅ | Identificador único do caso |
| `tipo_caso` | Choice | ✅ | 'humano' ou 'animal' |
| `sexo` | Choice | ✅ | 'masculino' ou 'feminino' |
| `gestante` | Boolean | ❌ | Se é gestante (apenas para fêmeas) |
| `data_nascimento` | Date | ❌ | Data de nascimento |
| `data_notificacao` | Date | ✅ | Data da notificação (padrão: hoje) |
| `municipio` | String(100) | ❌ | Nome do município |
| `latitude` | Float | ❌ | Coordenada de latitude |
| `longitude` | Float | ❌ | Coordenada de longitude |

#### Campos KalaCal Específicos
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `faixa_etaria_kalacal` | Choice | ❌ | Faixa etária para cálculo (1-5) |
| `sitios_sangramento` | Choice | ❌ | Número de sítios de sangramento (1-4) |
| `kalacal_habilitado` | Boolean | ❌ | Habilitado para análise KalaCal |

#### Sinais Clínicos (Boolean)
- `edema` - Presença de edema
- `aids` - Paciente com AIDS
- `ictericia` - Presença de icterícia
- `dispneia` - Presença de dispneia
- `infeccao` - Presença de infecção
- `vomitos` - Presença de vômitos

#### Dados Laboratoriais (Boolean)
- `leucopenia` - Presença de leucopenia
- `plaquetopenia` - Presença de plaquetopenia
- `insuficiencia_renal` - Presença de insuficiência renal
- `hepatite` - Presença de hepatite

### Choices/Enums

#### TipoCaso
```python
HUMANO = 'humano', 'Humano'
ANIMAL = 'animal', 'Animal'
```

#### Sexo
```python
MASCULINO = 'masculino', 'Masculino'
FEMININO = 'feminino', 'Feminino'
```

#### FaixaEtaria
```python
MENOR_12M = 1, '< 12 meses'
ENTRE_12_23M = 2, '12-23 meses'
ENTRE_2_15A = 3, '2-15 anos'
ENTRE_16_40A = 4, '16-40 anos'
MAIOR_40A = 5, '> 40 anos'
```

#### SitiosSangramento
```python
NENHUM = 1, 'Nenhum'
UM_DOIS = 2, '1-2 sítios'
TRES_QUATRO = 3, '3-4 sítios'
CINCO_SEIS = 4, '5-6 sítios'
```

### Endpoints de Casos

#### 1. Listar Casos
```http
GET /api/casos/
```

**Filtros Disponíveis:**
- `?tipo_caso=humano` ou `?tipo_caso=animal`
- `?sexo=masculino` ou `?sexo=feminino` 
- `?data_notificacao=2025-06-07`
- `?search=termo` (busca em identificador e município)
- `?kalacal_habilitado=true`

**Resposta:**
```json
[
    {
        "id": 1,
        "identificador": "H001",
        "tipo_caso": "humano",
        "tipo_display": "Humano",
        "data_nascimento": "1990-01-01",
        "sexo": "masculino",
        "gestante": false,
        "data_notificacao": "2025-06-07",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "municipio": "São Paulo",
        "faixa_etaria_kalacal": 4,
        "faixa_etaria_kalacal_display": "16-40 anos",
        "sitios_sangramento": 1,
        "sitios_sangramento_display": "Nenhum",
        "edema": false,
        "aids": false,
        "ictericia": false,
        "dispneia": false,
        "infeccao": false,
        "vomitos": false,
        "leucopenia": false,
        "plaquetopenia": false,
        "insuficiencia_renal": false,
        "hepatite": false,
        "kalacal_habilitado": true,
        "is_crianca_kalacal": false,
        "is_adulto_kalacal": true,
        "faixa_etaria_automatica": {
            "value": 4,
            "label": "16-40 anos"
        },
        "created_at": "2025-06-07T22:04:28.543256Z",
        "updated_at": "2025-06-07T22:04:28.543256Z"
    }
]
```

#### 2. Criar Caso
```http
POST /api/casos/
```

**Payload:**
```json
{
    "identificador": "KALA006",
    "tipo_caso": "humano",
    "sexo": "feminino",
    "gestante": false,
    "data_nascimento": "1985-05-15",
    "data_notificacao": "2025-06-07",
    "municipio": "Brasília",
    "latitude": -15.7939,
    "longitude": -47.8828,
    "faixa_etaria_kalacal": 4,
    "sitios_sangramento": 2,
    "edema": true,
    "aids": false,
    "kalacal_habilitado": true
}
```

#### 3. Obter Caso Específico
```http
GET /api/casos/{id}/
```

#### 4. Atualizar Caso
```http
PUT /api/casos/{id}/
PATCH /api/casos/{id}/
```

#### 5. Deletar Caso
```http
DELETE /api/casos/{id}/
```

#### 6. Estatísticas por Tipo
```http
GET /api/casos/por_tipo/
```

**Resposta:**
```json
{
    "humanos": 12,
    "animais": 5,
    "total": 17
}
```

---

## 🧮 APLICAÇÃO KALACAL_CALCULATOR

### Modelo Principal: `CalculoKalaCal`

Armazena histórico de cálculos de probabilidade realizados.

#### Campos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `caso` | ForeignKey | Referência ao caso |
| `modelo_usado` | Choice | 'clinico' ou 'clinico_laboratorial' |
| `escore` | Integer | Escore calculado (0-13) |
| `probabilidade_morte` | Float | Probabilidade de morte em % |
| `calculado_em` | DateTime | Timestamp do cálculo |
| `observacoes` | Text | Observações adicionais |

#### Choices do Modelo
```python
MODELO_CHOICES = [
    ('clinico', 'Clínico'),
    ('clinico_laboratorial', 'Clínico e Laboratorial'),
]
```

### Algoritmos Implementados

O sistema implementa 4 algoritmos distintos baseados em dados epidemiológicos:

1. **Clínico para crianças (< 2 anos)**: Escore 0-9
2. **Clínico + Laboratorial para crianças (< 2 anos)**: Escore 0-11
3. **Clínico para adultos (≥ 2 anos)**: Escore 0-13
4. **Clínico + Laboratorial para adultos (≥ 2 anos)**: Escore 0-10

#### Fatores de Pontuação

**Para Crianças (< 2 anos):**
- **Idade**: < 12 meses (+1 ponto)
- **Sangramento**: 1-2 sítios (+1), 3-4 sítios (+2), 5-6 sítios (+4)
- **Sinais**: Icterícia (+1), Dispneia (+1), Edema (+2)
- **Laboratorial**: Hepatite (+3)

**Para Adultos (≥ 2 anos):**
- **Idade**: 16-40 anos (+2), >40 anos (+3)
- **Sangramento**: 5-6 sítios (+3)
- **Sinais**: AIDS (+2), Edema (+1), Icterícia (+1), Dispneia (+1), Infecção (+1), Vômitos (+1)
- **Laboratorial**: Leucopenia (+1), Plaquetopenia (+2), Insuf. Renal (+2)

#### Interpretação dos Resultados
- **< 5%**: Risco baixo
- **5-20%**: Risco moderado
- **20-50%**: Risco alto
- **> 50%**: Risco muito alto

### Endpoints KalaCal

#### 1. Calcular Probabilidade (Endpoint Principal)
```http
POST /api/kalacal/calcular/
```

**Payload:**
```json
{
    "caso_id": "15",
    "modelo": "clinico",
    "faixa_etaria_kalacal": 3,
    "sitios_sangramento": 2,
    "edema": true,
    "aids": false,
    "ictericia": false,
    "dispneia": true,
    "infeccao": false,
    "vomitos": false,
    "leucopenia": false,
    "plaquetopenia": false,
    "insuficiencia_renal": false,
    "hepatite": false,
    "observacoes": "Cálculo de exemplo"
}
```

**Resposta:**
```json
{
    "caso_id": 15,
    "escore": 3,
    "escore_maximo": 13,
    "probabilidade_morte": 6.5,
    "modelo_usado": "clinico",
    "interpretacao": "Risco moderado",
    "calculo_id": 23,
    "calculado_em": "2025-06-08T15:30:45.123456Z"
}
```

**Notas:**
- `caso_id` pode ser ID numérico ou identificador string
- Campos opcionais atualizam o caso antes do cálculo
- Cálculo é automaticamente salvo no histórico

#### 2. Opções para Formulários
```http
GET /api/kalacal/opcoes/
```

**Resposta:**
```json
{
    "faixas_etarias": [
        {"value": 1, "label": "< 12 meses"},
        {"value": 2, "label": "12-23 meses"},
        {"value": 3, "label": "2-15 anos"},
        {"value": 4, "label": "16-40 anos"},
        {"value": 5, "label": "> 40 anos"}
    ],
    "sitios_sangramento": [
        {"value": 1, "label": "Nenhum"},
        {"value": 2, "label": "1-2 sítios"},
        {"value": 3, "label": "3-4 sítios"},
        {"value": 4, "label": "5-6 sítios"}
    ],
    "modelos": [
        {"value": "clinico", "label": "Clínico"},
        {"value": "clinico_laboratorial", "label": "Clínico e Laboratorial"}
    ],
    "sinais_clinicos": [
        {"key": "edema", "label": "Edema"},
        {"key": "aids", "label": "AIDS"},
        {"key": "ictericia", "label": "Icterícia"},
        {"key": "dispneia", "label": "Dispneia"},
        {"key": "infeccao", "label": "Infecção"},
        {"key": "vomitos", "label": "Vômitos"}
    ],
    "dados_laboratoriais": [
        {"key": "leucopenia", "label": "Leucopenia"},
        {"key": "plaquetopenia", "label": "Plaquetopenia"},
        {"key": "insuficiencia_renal", "label": "Insuficiência Renal"},
        {"key": "hepatite", "label": "Hepatite"}
    ]
}
```

#### 3. Métricas do Sistema
```http
GET /api/kalacal/metricas/
```

**Resposta:**
```json
{
    "total_calculos": 45,
    "total_casos_com_calculos": 23,
    "calculos_por_modelo": {
        "clinico": 28,
        "clinico_laboratorial": 17
    },
    "calculos_por_faixa_etaria": {
        "1": 5,
        "2": 8,
        "3": 15,
        "4": 12,
        "5": 5
    },
    "media_probabilidade": {
        "clinico": 12.4,
        "clinico_laboratorial": 8.7
    },
    "distribuicao_escores": {
        "0": 3,
        "1": 5,
        "2": 8,
        "3": 12,
        "4": 7,
        "5": 10
    },
    "casos_por_interpretacao": {
        "Risco baixo": 15,
        "Risco moderado": 18,
        "Risco alto": 8,
        "Risco muito alto": 4
    }
}
```

#### 4. Casos com Cálculos
```http
GET /api/kalacal/casos/
```

Lista casos que possuem pelo menos um cálculo realizado.

**Filtros:** Mesmos filtros dos casos normais.

#### 5. Histórico de Caso
```http
GET /api/kalacal/casos/{caso_id}/historico/
```

**Parâmetros:**
- `caso_id`: ID numérico ou identificador string

**Resposta:**
```json
{
    "caso": {
        "id": 15,
        "identificador": "KALA003",
        "tipo_display": "Humano",
        "faixa_etaria_kalacal": 3,
        "faixa_etaria_kalacal_display": "2-15 anos",
        "sitios_sangramento": 1,
        "sitios_sangramento_display": "Nenhum",
        "edema": false,
        "aids": false,
        "ictericia": false,
        "dispneia": true,
        "infeccao": false,
        "vomitos": false,
        "leucopenia": false,
        "plaquetopenia": false,
        "insuficiencia_renal": false,
        "hepatite": false,
        "kalacal_habilitado": true,
        "dados_kalacal": {
            "faixa_etaria": 3,
            "sitios_sangramento": 1,
            "edema": false,
            "aids": false,
            "ictericia": false,
            "dispneia": true,
            "infeccao": false,
            "vomitos": false,
            "leucopenia": false,
            "plaquetopenia": false,
            "insuficiencia_renal": false,
            "hepatite": false
        }
    },
    "historico_calculos": [
        {
            "id": 23,
            "caso_identificador": "KALA003",
            "caso_municipio": "Teresina",
            "modelo_usado": "clinico",
            "modelo_usado_display": "Clínico",
            "escore": 1,
            "probabilidade_morte": 3.6,
            "interpretacao": "Risco baixo",
            "calculado_em": "2025-06-08T15:30:45.123456Z",
            "observacoes": "Primeiro cálculo"
        },
        {
            "id": 24,
            "caso_identificador": "KALA003",
            "caso_municipio": "Teresina",
            "modelo_usado": "clinico_laboratorial",
            "modelo_usado_display": "Clínico e Laboratorial",
            "escore": 1,
            "probabilidade_morte": 3.0,
            "interpretacao": "Risco baixo",
            "calculado_em": "2025-06-08T15:35:12.456789Z",
            "observacoes": "Cálculo com dados laboratoriais"
        }
    ],
    "total_calculos": 2
}
```

#### 6. Lista de Cálculos
```http
GET /api/kalacal/calculos/
```

**Filtros:**
- `?modelo=clinico` ou `?modelo=clinico_laboratorial`
- `?caso_id=15`

**Resposta:**
```json
[
    {
        "id": 23,
        "caso_identificador": "KALA003",
        "caso_municipio": "Teresina",
        "modelo_usado": "clinico",
        "modelo_usado_display": "Clínico",
        "escore": 1,
        "probabilidade_morte": 3.6,
        "interpretacao": "Risco baixo",
        "calculado_em": "2025-06-08T15:30:45.123456Z",
        "observacoes": "Primeiro cálculo"
    }
]
```

---

## 🔧 CONFIGURAÇÃO E DESENVOLVIMENTO

### CORS
A API está configurada para aceitar requisições de:
- `http://localhost:8081` (Expo dev server)
- `http://10.0.2.2:8000` (Emulador Android)
- Qualquer origem (para desenvolvimento)

### Comandos de Inicialização

#### Iniciar Servidor
```bash
python manage.py runserver 0.0.0.0:8000
```

#### Popular Dados de Exemplo
```bash
# Casos básicos
python manage.py populate_casos

# Casos com cálculos KalaCal
python manage.py populate_kalacal
```

#### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Interface Admin

Acesse em: `http://localhost:8000/admin/`

**Funcionalidades:**
- Gerenciamento completo de casos
- Visualização de cálculos
- Filtros avançados
- Ações em lote para habilitar/desabilitar KalaCal

---

## 📋 EXEMPLOS DE USO

### Cenário 1: Criança com Risco Alto
```bash
# 1. Criar caso pediátrico
curl -X POST http://localhost:8000/api/casos/ \
  -H "Content-Type: application/json" \
  -d '{
    "identificador": "PEDIATRICO001",
    "tipo_caso": "humano",
    "sexo": "masculino",
    "data_nascimento": "2024-01-15",
    "municipio": "Teresina",
    "faixa_etaria_kalacal": 1,
    "sitios_sangramento": 4,
    "edema": true,
    "ictericia": true,
    "dispneia": true,
    "hepatite": true
  }'

# 2. Calcular probabilidade (modelo clínico+laboratorial)
curl -X POST http://localhost:8000/api/kalacal/calcular/ \
  -H "Content-Type: application/json" \
  -d '{
    "caso_id": "PEDIATRICO001",
    "modelo": "clinico_laboratorial"
  }'
```

### Cenário 2: Adulto com Múltiplos Fatores
```bash
# 1. Criar caso adulto
curl -X POST http://localhost:8000/api/casos/ \
  -H "Content-Type: application/json" \
  -d '{
    "identificador": "ADULTO001",
    "tipo_caso": "humano",
    "sexo": "feminino",
    "data_nascimento": "1975-05-20",
    "municipio": "Fortaleza",
    "faixa_etaria_kalacal": 5,
    "sitios_sangramento": 4,
    "aids": true,
    "edema": true,
    "ictericia": true,
    "vomitos": true,
    "leucopenia": true,
    "plaquetopenia": true
  }'

# 2. Calcular probabilidade (modelo clínico)
curl -X POST http://localhost:8000/api/kalacal/calcular/ \
  -H "Content-Type: application/json" \
  -d '{
    "caso_id": "ADULTO001",
    "modelo": "clinico",
    "observacoes": "Paciente com múltiplos fatores de risco"
  }'
```

### Cenário 3: Análise de Histórico
```bash
# Verificar histórico de cálculos do caso
curl http://localhost:8000/api/kalacal/casos/ADULTO001/historico/

# Obter métricas gerais do sistema
curl http://localhost:8000/api/kalacal/metricas/

# Listar todos os cálculos do modelo clínico
curl http://localhost:8000/api/kalacal/calculos/?modelo=clinico
```

---

## ⚠️ CÓDIGOS DE ERRO COMUNS

### HTTP 400 - Bad Request
```json
{
    "error": "Faixa etária é obrigatória. Defina faixa_etaria_kalacal ou data_nascimento no caso."
}
```

### HTTP 404 - Not Found
```json
{
    "error": "Caso não encontrado"
}
```

### HTTP 500 - Internal Server Error
```json
{
    "error": "Erro no cálculo: [detalhes do erro]"
}
```

---

## 📚 FUNDAMENTAÇÃO CIENTÍFICA

### Base Epidemiológica
Os algoritmos foram desenvolvidos com base em estudo epidemiológico realizado em Teresina-PI entre 2005-2013, analisando fatores preditivos de morte em pacientes com Kala-azar.

### Validação
- Algoritmos validados contra dados reais de mortalidade
- Curvas de probabilidade ajustadas por regressão logística
- Separação por faixas etárias devido a diferentes padrões de mortalidade

### Limitações
- Dados específicos da região de Teresina-PI
- Período de coleta: 2005-2013
- Aplicabilidade pode variar em outras populações

---

## 🚀 ROADMAP E MELHORIAS FUTURAS

### Versão Atual (v1.0)
- ✅ Cálculos epidemiológicos básicos
- ✅ API REST completa
- ✅ Interface administrativa
- ✅ Histórico de cálculos

### Próximas Versões
- 🔄 Validação de dados em tempo real
- 🔄 Exportação de relatórios
- 🔄 Integração com sistemas de saúde
- 🔄 APIs de geolocalização avançada
- 🔄 Dashboard analítico

---

## 📞 SUPORTE

Para questões técnicas ou científicas sobre o sistema KalaKal, consulte:
- Documentação do código fonte
- Logs de aplicação em desenvolvimento
- Artigos científicos sobre Kala-azar epidemiológico

---

*Última atualização: Junho 2025*
*Versão da API: 1.0*
*Django: 5.2.2*
*Python: 3.x* 