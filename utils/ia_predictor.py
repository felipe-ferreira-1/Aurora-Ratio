from transformers import pipeline
from utils.market_data import buscar_dados_mercado, historico_7_dias

# 🚀 Carrega pipeline de sentimento (simples e multilíngue)
sentiment = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analisar_texto(texto: str) -> str:
    """
    Classifica sentimento geral do texto em BUY / HOLD / SELL
    usando modelo de linguagem treinado em avaliações.
    """
    if not texto.strip():
        return "neutro"

    resultado = sentiment(texto[:512])[0]  # protege contra excesso de tokens
    label = resultado["label"]

    # Modelo retorna estrelas: '1 star' a '5 stars'
    if "5" in label or "4" in label:
        return "buy"
    elif "3" in label:
        return "hold"
    elif "1" in label or "2" in label:
        return "sell"
    else:
        return "neutro"


def sugestao_com_dados(texto: str, ticker: str) -> str:
    """
    Retorna sugestão ajustada com base no texto + dados reais do mercado
    """
    try:
        # 1️⃣ Sugestão baseada no texto dos alertas + comentários
        base = analisar_texto(texto)

        # 2️⃣ Dados reais de mercado
        fontes = buscar_dados_mercado(ticker)
        preco_atual = list(fontes.values())[0].get("preco", 0) if fontes else 0

        # 3️⃣ Histórico dos últimos 7 dias
        df_hist = historico_7_dias(ticker)
        if df_hist.empty:
            return base

        preco_inicial = df_hist["fechamento"].iloc[0]
        delta = preco_atual - preco_inicial

        # 4️⃣ Ajuste estratégico
        if delta > 1 and base == "buy":
            return "buy"
        elif delta < -1 and base == "buy":
            return "hold"
        elif delta < -2:
            return "sell"
        else:
            return base

    except Exception as e:
        print(f"Erro IA preditiva: {e}")
        return "neutro"