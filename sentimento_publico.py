from transformers import pipeline
sentiment = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

def analisar_tweets(tweets):
    resultados = sentiment(tweets[:5])
    positivos = sum(1 for r in resultados if "POSITIVE" in r["label"])
    negativos = sum(1 for r in resultados if "NEGATIVE" in r["label"])
    neutros = len(resultados) - positivos - negativos
    return {"positivo": positivos, "negativo": negativos, "neutro": neutros}