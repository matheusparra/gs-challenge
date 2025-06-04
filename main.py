from src.preprocessamento import carregar_dados
from src.treino_modelo import treinar_modelo

df = carregar_dados("data/dados_enchentes.csv")
treinar_modelo(df)
