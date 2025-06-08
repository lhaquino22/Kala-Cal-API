#!/usr/bin/env python3
"""
Exemplo de uso da API KalaCal
Demonstra como consumir os endpoints para calcular probabilidade de morte
"""

import requests
import json

# Configuração da API
API_BASE_URL = "http://localhost:8000/api/kalacal"

def testar_opcoes_formulario():
    """Testa o endpoint de opções do formulário"""
    print("=== Testando opções do formulário ===")
    
    response = requests.get(f"{API_BASE_URL}/opcoes/")
    
    if response.status_code == 200:
        opcoes = response.json()
        print("✅ Opções obtidas com sucesso!")
        print(f"Faixas etárias disponíveis: {len(opcoes['faixas_etarias'])}")
        print(f"Modelos disponíveis: {len(opcoes['modelos'])}")
        print(f"Sinais clínicos: {len(opcoes['sinais_clinicos'])}")
        return opcoes
    else:
        print(f"❌ Erro ao obter opções: {response.status_code}")
        return None

def calcular_probabilidade_exemplo():
    """Testa o cálculo de probabilidade com dados de exemplo"""
    print("\n=== Testando cálculo de probabilidade ===")
    
    # Exemplo 1: Criança com risco moderado
    dados_crianca = {
        "faixa_etaria": 1,  # < 12 meses
        "sitios_sangramento": 2,  # 1-2 sítios
        "modelo": "clinico",
        "edema": True,
        "aids": False,
        "ictericia": True,
        "dispneia": False,
        "infeccao": False,
        "vomitos": False,
        "leucopenia": False,
        "plaquetopenia": False,
        "insuficiencia_renal": False,
        "hepatite": False,
        "nome": "Bebê Exemplo",
        "salvar_paciente": True
    }
    
    response = requests.post(
        f"{API_BASE_URL}/calcular/",
        json=dados_crianca,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        resultado = response.json()
        print("✅ Cálculo realizado com sucesso!")
        print(f"Paciente: {dados_crianca['nome']}")
        print(f"Faixa etária: {resultado['faixa_etaria_display']}")
        print(f"Escore: {resultado['escore']}/{resultado['escore_maximo']}")
        print(f"Probabilidade de morte: {resultado['probabilidade_morte']}%")
        print(f"Interpretação: {resultado['interpretacao']}")
        print(f"Paciente salvo com ID: {resultado['paciente_id']}")
        return resultado
    else:
        print(f"❌ Erro no cálculo: {response.status_code}")
        print(response.text)
        return None

def calcular_adulto_laboratorial():
    """Testa cálculo para adulto com dados laboratoriais"""
    print("\n=== Testando adulto com dados laboratoriais ===")
    
    dados_adulto = {
        "faixa_etaria": 4,  # 16-40 anos
        "sitios_sangramento": 4,  # 5-6 sítios
        "modelo": "clinico_laboratorial",
        "edema": False,
        "aids": False,
        "ictericia": True,
        "dispneia": True,
        "infeccao": True,
        "vomitos": False,
        "leucopenia": True,
        "plaquetopenia": True,
        "insuficiencia_renal": False,
        "hepatite": False,
        "nome": "Adulto Alto Risco",
        "salvar_paciente": True
    }
    
    response = requests.post(
        f"{API_BASE_URL}/calcular/",
        json=dados_adulto,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        resultado = response.json()
        print("✅ Cálculo adulto realizado com sucesso!")
        print(f"Paciente: {dados_adulto['nome']}")
        print(f"Modelo: {resultado['modelo_usado']}")
        print(f"Escore: {resultado['escore']}/{resultado['escore_maximo']}")
        print(f"Probabilidade de morte: {resultado['probabilidade_morte']}%")
        print(f"Interpretação: {resultado['interpretacao']}")
        return resultado
    else:
        print(f"❌ Erro no cálculo adulto: {response.status_code}")
        return None

def listar_pacientes():
    """Lista todos os pacientes cadastrados"""
    print("\n=== Listando pacientes ===")
    
    response = requests.get(f"{API_BASE_URL}/pacientes/")
    
    if response.status_code == 200:
        pacientes = response.json()
        print(f"✅ Total de pacientes: {len(pacientes)}")
        for paciente in pacientes:
            print(f"- {paciente['nome']} ({paciente['faixa_etaria_display']})")
        return pacientes
    else:
        print(f"❌ Erro ao listar pacientes: {response.status_code}")
        return None

def obter_metricas():
    """Obtém métricas do sistema"""
    print("\n=== Obtendo métricas do sistema ===")
    
    response = requests.get(f"{API_BASE_URL}/metricas/")
    
    if response.status_code == 200:
        metricas = response.json()
        print("✅ Métricas obtidas com sucesso!")
        print(f"Total de cálculos: {metricas['total_calculos']}")
        print("Cálculos por modelo:")
        for modelo, count in metricas['calculos_por_modelo'].items():
            print(f"  - {modelo}: {count}")
        print("Média de probabilidade por modelo:")
        for modelo, media in metricas['media_probabilidade'].items():
            print(f"  - {modelo}: {media}%")
        return metricas
    else:
        print(f"❌ Erro ao obter métricas: {response.status_code}")
        return None

def main():
    """Executa todos os testes"""
    print("🧮 Testando API KalaCal - Calculadora de Probabilidade de Morte")
    print("="*60)
    
    try:
        # Testa os endpoints
        opcoes = testar_opcoes_formulario()
        resultado1 = calcular_probabilidade_exemplo()
        resultado2 = calcular_adulto_laboratorial()
        pacientes = listar_pacientes()
        metricas = obter_metricas()
        
        print("\n" + "="*60)
        print("✅ Todos os testes concluídos!")
        print("\nPara usar no seu frontend, você pode:")
        print("1. Chamar /opcoes/ para construir formulários dinâmicos")
        print("2. Enviar dados para /calcular/ para obter probabilidades")
        print("3. Usar /pacientes/ para gerenciar pacientes")
        print("4. Consultar /metricas/ para estatísticas do sistema")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão! Certifique-se de que o servidor está rodando:")
        print("python manage.py runserver 0.0.0.0:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main() 