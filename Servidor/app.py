from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
modelo = joblib.load("../modelo/modelo_random_forest.joblib")

@app.route('/dados', methods=['POST'])
def prever():
    try:
        dados = request.get_json()
        df = pd.DataFrame([dados])
        risco = modelo.predict(df)[0]
        prob = modelo.predict_proba(df)[0][1] * 100

        print(f"📥 Dados recebidos: {dados}")
        print(f"🧠 Risco previsto: {'ALTO' if risco == 1 else 'BAIXO'} ({prob:.2f}%)")

        return jsonify({
            "risco": int(risco),
            "probabilidade": round(prob, 2)
        })
    
    except Exception as e:
        print("❌ Erro interno:", e)
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
