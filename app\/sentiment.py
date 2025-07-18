import os
from dotenv import load_dotenv

# 🔮 Seletor de IA
MODO_IA = os.getenv("MODO_IA", "local")  # Opções: local, huggingface, openai

# 🧠 IA local (baseada em palavras-chave)
def analisar_local(texto: str) -> str:
    texto = texto.lower()
    positivos = ["crescimento", "lucro", "expansão", "parceria", "investimento", "recorde", "contrato"]
    negativos = ["queda", "demissão", "prejuízo", "crise", "falência", "processo", "fraude"]

    if any(p in texto for p in positivos):
        return "positivo"
    elif any(n in texto for n in negativos):
        return "negativo"
    else:
        return "neutro"

# 🧪 IA via Hugging Face
def analisar_huggingface(texto: str) -> str:
    try:
        from transformers import pipeline
        classificador = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
        resultado = classificador(texto[:512])[0]['label']
        if "1 star" in resultado or "2 stars" in resultado:
            return "negativo"
        elif "3 stars" in resultado:
            return "neutro"
        else:
            return "positivo"
    except Exception as e:
        print(f"⚠️ Erro com Hugging Face: {e}")
        return "neutro"

# 🔐 IA via OpenAI
def analisar_openai(texto: str) -> str:
    try:
        import openai
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        prompt = f"Classifique o sentimento da seguinte manchete como positivo, negativo ou neutro:\n\"{texto}\""
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        conteudo = resposta.choices[0].message.content.lower()
        if "positivo" in conteudo:
            return "positivo"
        elif "negativo" in conteudo:
            return "negativo"
        else:
            return "neutro"
    except Exception as e:
        print(f"⚠️ Erro com OpenAI: {e}")
        return "neutro"

# 🤖 Função principal com seletor
def analisar_sentimento(texto: str) -> str:
    modo = MODO_IA.lower()

    if modo == "huggingface":
        return analisar_huggingface(texto)
    elif modo == "openai":
        return analisar_openai(texto)
    else:
        return analisar_local(texto)