import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

# 🔮 Seletor de IA
MODO_IA = os.getenv("MODO_IA", "local").lower()  # Opções: local, huggingface, openai

# ✅ Validação básica
def validar_texto(texto: str) -> bool:
    return isinstance(texto, str) and len(texto.strip()) > 0

# 🧠 IA local baseada em palavras-chave
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
        import os
        from transformers import pipeline
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("HUGGINGFACE_API_KEY")

        classificador = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", api_key=api_key)
        resultado = classificador("O mercado está em queda livre.")
        print(resultado)

# 🧪 IA via Hugging Face
def analisar_huggingface(texto: str) -> str:
    try:
        from transformers import pipeline # pyright: ignore[reportMissingImports]
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
        import openai # pyright: ignore[reportMissingImports]
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
    if not validar_texto(texto):
        return "neutro"

    if MODO_IA == "huggingface":
        return analisar_huggingface(texto)
    elif MODO_IA == "openai":
        return analisar_openai(texto)
    else:
        return analisar_local(texto)

# 📊 Retorno estruturado enriquecido
def analisar_sentimento_rico(texto: str) -> dict:
    resultado = analisar_sentimento(texto)
    return {
        "texto": texto,
        "sentimento": resultado,
        "modo_ia": MODO_IA
    }

# 🧾 Auditoria via Supabase
def registrar_log_sentimento(texto: str, resultado: dict):
    try:
        from supabase import create_client # pyright: ignore[reportMissingImports]
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        chave = os.getenv("SUPABASE_KEY")
        supabase = create_client(url, chave)

        supabase.table("logs_sentimento").insert({
            "texto": texto,
            "sentimento": resultado.get("sentimento"),
            "fonte": resultado.get("fonte"),
            "confiança": resultado.get("confiança"),
            "mensagem": resultado.get("mensagem"),
            "timestamp": datetime.now().isoformat() # pyright: ignore[reportUndefinedVariable]
        }).execute()
    except Exception as e:
        print(f"⚠️ Erro ao registrar log: {e}")
        