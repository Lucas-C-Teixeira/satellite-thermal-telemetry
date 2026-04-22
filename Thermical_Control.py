import matplotlib.pyplot as plt
import math
import random
from typing import List, Dict, Tuple

# Constantes globais facilitam a manutenção do sistema
TEMP_MIN_VALIDA = -100
TEMP_MAX_VALIDA = 120

def gerar_dados(duracao: int, intervalo: int, periodo_orbita: int) -> List[Dict]:
    """
    Simula a telemetria térmica de um satélite usando uma onda senoidal com ruído.
    """
    offset = 15.0
    amplitude = 60
    w = (2 * math.pi) / periodo_orbita

    dados = []
    for i in range(0, duracao + 1, intervalo):
        # Base senoidal + ruído gaussiano (mais realista que uniform)
        medicao_base = offset + (amplitude * math.sin(w * i))
        ruido = random.uniform(-2, 2)
        
        dados.append({
            "minuto": i, 
            "temp": round(medicao_base + ruido, 2)
        })
    return dados

def processar_telemetria(dados: List[Dict]) -> List[Dict]:
    """
    Valida e classifica os dados em uma única passagem para otimizar performance.
    """
    dados_processados = []
    
    for medicao in dados:
        temp = medicao['temp']
        
        # Validação de integridade do sensor
        if not (TEMP_MIN_VALIDA <= temp <= TEMP_MAX_VALIDA):
            print(f"[ALERTA] Sensor corrompido no minuto {medicao['minuto']}: {temp}°C")
            continue

        # Classificação (Dicionário de faixas para evitar muitos if/else)
        if temp < -40: status = "Cold Case Crítico"
        elif temp <= -20: status = "Frio"
        elif temp <= 50:  status = "Nominal"
        elif temp <= 70:  status = "Quente"
        else: status = "Hot Case Crítico"
        
        medicao['status'] = status
        dados_processados.append(medicao)
        
    return dados_processados

def detectar_extremos(dados: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """Identifica picos (máximos locais) e vales (mínimos locais)."""
    picos = [dados[i] for i in range(1, len(dados)-1) 
             if dados[i-1]['temp'] < dados[i]['temp'] > dados[i+1]['temp']]
    
    vales = [dados[i] for i in range(1, len(dados)-1) 
             if dados[i-1]['temp'] > dados[i]['temp'] < dados[i+1]['temp']]
    
    return picos, vales

def exibir_dashboard(dados: List[Dict], picos: List[Dict], vales: List[Dict]):
    """Gera o relatório textual e visual dos dados."""
    temps = [d['temp'] for d in dados]
    
    # Estatísticas rápidas
    stats = {
        "Máxima": max(temps),
        "Mínima": min(temps),
        "Média": sum(temps) / len(temps)
    }

    print("\n" + "="*30)
    print("      RELATÓRIO TÉRMICO")
    print("="*30)
    for k, v in stats.items():
        print(f"{k:10}: {v:>6.2f}°C")
    print(f"Picos det.: {len(picos)} | Vales det.: {len(vales)}")
    print("="*30)

    # Plotagem Profissional
    plt.figure(figsize=(12, 6))
    minutos = [d['minuto'] for d in dados]
    
    plt.plot(minutos, temps, color='#2c3e50', label='Telemetria Real-time', alpha=0.7)
    
    # Destaque de Picos e Vales com marcadores mais visíveis
    plt.scatter([p['minuto'] for p in picos], [p['temp'] for p in picos], 
                color='red', marker='^', label='Picos de Calor')
    plt.scatter([v['minuto'] for v in vales], [v['temp'] for v in vales], 
                color='blue', marker='v', label='Vales de Resfriamento')

    plt.title("Monitoramento Térmico Orbital", fontsize=14)
    plt.xlabel("Tempo (minutos)")
    plt.ylabel("Temperatura (°C)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# --- EXECUÇÃO DO SCRIPT ---
if __name__ == "__main__":
    # Configurações de simulação
    DURACAO_MISSAO = 160 # min
    INTERVALO_LEITURA = 3 # min
    PERIODO_ORBITA = 90 # min (padrão ISS)

    raw_data = gerar_dados(DURACAO_MISSAO, INTERVALO_LEITURA, PERIODO_ORBITA)
    clean_data = processar_telemetria(raw_data)
    picos, vales = detectar_extremos(clean_data)
    
    exibir_dashboard(clean_data, picos, vales)
    