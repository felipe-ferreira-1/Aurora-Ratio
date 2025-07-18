import os
from datetime import datetime
from app.sentiment import analisar_sentimento
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
from app.notificador import enviar_alerta_email
from app.alerta_popup import emitir_popup

# 🔧 Carrega variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"

# 📥 Buscar empresas com monitoramento ativado direto do Supabase
def carregar_empresas_monitoradas():
    try:
        resposta = supabase.table("empresas").select("nome").eq("monitorar", True).execute()
        return [linha["nome"] for linha in resposta.data]
    except Exception as e:
        print(f"⚠️ Erro ao carregar empresas monitoradas: {e}")
        return []

# 🧠 Validação semântica
def manchete_valida(manchete: str) -> bool:
    if not manchete or len(manchete.strip()) < 10:
        return False
    blacklist = ["...", "sem título", "unknown", "http", "imagem"]
    if any(p in manchete.lower() for p in blacklist):
        return False
    return True

# 🔁 Checagem por duplicatas
def alerta_ja_existente(manchete: str) -> bool:
    try:
        resultado = supabase.table("alertas").select("noticia").eq("noticia", manchete).execute()
        return bool(resultado.data)
    except:
        return False

# 🌐 Buscar manchetes
def buscar_manchetes_por_api(empresas):
    query = " OR ".join(empresas)
    url = f"{NEWSAPI_ENDPOINT}?q={query}&language=pt&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        artigos = dados.get("articles", [])
        return [art["title"] for art in artigos if "title" in art]
    except Exception as e:
        print(f"⚠️ Erro na NewsAPI: {e}")
        return []

# 📡 Função principal
def monitorar_noticias():
    empresas = carregar_empresas_monitoradas()
    manchetes = buscar_manchetes_por_api(empresas)
    print("📡 Monitoramento iniciado...\n")

    for noticia in manchetes:
        if not manchete_valida(noticia):
            print(f"🚫 Manchete inválida: {noticia}")
            continue