import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Carregar modelo
modelo = joblib.load("modelo/modelo_random_forest.joblib")

st.set_page_config(page_title="Monitor de Enchentes", layout="centered")
st.title("🌧️ Monitor Inteligente de Risco de Enchente")

st.markdown("Envie dados manualmente ou conecte com ESP32/simulador.")

# Entradas de dados simulados ou manuais
with st.form("formulario_dados"):
    chuva_1h = st.slider("Chuva (1h)", 0.0, 50.0, 10.0)
    chuva_6h = st.slider("Chuva (6h)", 0.0, 100.0, 30.0)
    chuva_24h = st.slider("Chuva (24h)", 0.0, 200.0, 60.0)
    nivel_rio = st.slider("Nível do Rio (m)", 0.0, 10.0, 4.5)
    tendencia_rio = st.selectbox("Tendência do Rio", [0, 1])
    umidade = st.slider("Umidade (%)", 30.0, 100.0, 85.0)
    vento = st.slider("Velocidade do Vento (km/h)", 0.0, 40.0, 10.0)
    
    enviar = st.form_submit_button("🔍 Analisar Risco")

if enviar:
    dados = {
        "chuva_1h": chuva_1h,
        "chuva_6h": chuva_6h,
        "chuva_24h": chuva_24h,
        "nivel_rio": nivel_rio,
        "tendencia_rio": tendencia_rio,
        "umidade": umidade,
        "vento": vento
    }

    df = pd.DataFrame([dados])
    risco = modelo.predict(df)[0]
    prob = modelo.predict_proba(df)[0][1] * 100

    st.subheader("Resultado da Previsão")
    st.metric("Probabilidade de Enchente", f"{prob:.2f}%")

    if risco == 1 and prob >= 80:
        st.error("⚠️ ALERTA: Alto risco de enchente!")
    else:
        st.success("✅ Sem risco significativo detectado.")

    st.markdown("**Dados analisados:**")
    st.dataframe(df)
