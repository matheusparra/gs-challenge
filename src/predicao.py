import joblib
import pandas as pd

# Carrega o modelo treinado
modelo = joblib.load('models/modelo_random_forest.joblib')

def prever_risco(dados_sensor):
    """
    Recebe um dicionário com os dados do sensor e retorna a predição e o risco (%).
    """
    df = pd.DataFrame([dados_sensor])
    risco = modelo.predict(df)[0]
    probabilidade = modelo.predict_proba(df)[0][1] * 100  # Probabilidade de risco (classe 1)

    print(f"Risco previsto: {'ALTO' if risco == 1 else 'BAIXO'} ({probabilidade:.2f}%)")
    return risco, probabilidade
