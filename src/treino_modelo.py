from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score
import joblib

def treinar_modelo(df):
    X = df.drop(columns=['risco_enchente'])
    y = df['risco_enchente']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    modelo = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    print(f"Acurácia: {accuracy_score(y_test, y_pred)}")
    print(f"Recall: {recall_score(y_test, y_pred)}")

    joblib.dump(modelo, "modelo/modelo_random_forest.joblib")

