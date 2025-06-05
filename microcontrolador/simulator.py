import requests
import time
import random

# URL da sua API Flask local
URL = "http://localhost:5000/dados"

def gerar_dados_simulados():
    return {
        "chuva_1h": round(random.uniform(0.0, 30.0), 2),
        "chuva_6h": round(random.uniform(0.0, 60.0), 2),           # ✅ necessário
        "chuva_24h": round(random.uniform(0.0, 100.0), 2),
        "nivel_rio": round(random.uniform(2.0, 8.0), 2),
        "tendencia_rio": random.choice([0, 1]),                    # ✅ necessário
        "umidade": round(random.uniform(60.0, 95.0), 2),
        "vento": round(random.uniform(0.0, 20.0), 2)
    }

while True:
    dados = gerar_dados_simulados()
    print("📤 Enviando dados simulados:", dados)

    try:
        resposta = requests.post(URL, json=dados)
        print("✅ Resposta do servidor:", resposta.status_code)
        print("🔁 Conteúdo:", resposta.text)
    except Exception as e:
        print("❌ Erro ao enviar:", e)

    time.sleep(5)  # Aguarda 5 segundos para nova simulação
