import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# 🔐 API Keys carregadas do .env
FINNHUB_KEY = os.getenv("FINNHUB_KEY")
ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")
FMP_KEY = os.getenv("FMP_KEY")


# ✅ Finnhub
def dados_finnhub(ticker):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
        res = requests.get(url, timeout=6).json()
        return {
            "fonte": "Finnhub",
            "preco": res.get("c"),
            "variacao": round(res.get("dp", 0), 2),
            "abertura": res.get("o"),
            "fechamento": res.get("pc"),
            "volume": None,
            "marketCap": None
        }
    except Exception as e:
        print(f"Finnhub falhou: {e}")
        return None


# ✅ Alpha Vantage
def dados_alpha(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_KEY}"
        res = requests.get(url, timeout=6).json().get("Global Quote", {})
        return {
            "fonte": "Alpha Vantage",
            "preco": float(res.get("05. price", 0)),
            "variacao": float(res.get("10. change percent", "0%").replace("%", "")),
            "volume": int(res.get("06. volume", 0)),
            "abertura": float(res.get("02. open", 0)),
            "fechamento": float(res.get("08. previous close", 0)),
            "marketCap": None
        }
    except Exception as e:
        print(f"Alpha Vantage falhou: {e}")
        return None


# ✅ Financial Modeling Prep (FMP)
def dados_fmp(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP_KEY}"
        res = requests.get(url, timeout=6).json()
        info = res[0] if res else {}
        return {
            "fonte": "FMP",
            "preco": info.get("price"),
            "variacao": round(info.get("changesPercentage", 0), 2),
            "volume": info.get("volume"),
            "marketCap": info.get("marketCap"),
            "abertura": info.get("open"),
            "fechamento": info.get("previousClose")
        }
    except Exception as e:
        print(f"FMP falhou: {e}")
        return None


# 🔄 Fallback inteligente: só retorna fontes válidas
def buscar_dados_mercado(ticker):
    fontes_disponiveis = {}

    fmp = dados_fmp(ticker)
    if fmp: fontes_disponiveis["fmp"] = fmp

    alpha = dados_alpha(ticker)
    if alpha: fontes_disponiveis["alpha"] = alpha

    finnhub = dados_finnhub(ticker)
    if finnhub: fontes_disponiveis["finnhub"] = finnhub

    return fontes_disponiveis


# 🎯 Comparador entre fontes
def comparar_fontes(dados):
    comparativo = []
    for fonte, info in dados.items():
        comparativo.append({
            "fonte": info.get("fonte"),
            "preco": info.get("preco"),
            "variacao": info.get("variacao")
        })
    return pd.DataFrame(comparativo)


# 📉 Histórico de fechamento dos últimos 7 dias (Alpha Vantage)
def historico_7_dias(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_KEY}"
        res = requests.get(url, timeout=6).json().get("Time Series (Daily)", {})
        dados = []
        for data, valores in list(res.items())[:7]:
            dados.append({
                "data": data,
                "fechamento": float(valores["4. close"])
            })
        return pd.DataFrame(dados[::-1])  # do mais antigo para o mais recente
    except Exception as e:
        print(f"Histórico falhou: {e}")
        return pd.DataFrame()