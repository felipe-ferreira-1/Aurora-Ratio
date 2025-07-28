import os
from datetime import datetime
from app.sentiment import analisar_sentimento # pyright: ignore[reportMissingImports]
from supabase import create_client, Client # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
import requests # pyright: ignore[reportMissingModuleSource]
from app.notificador import enviar_alerta_email # pyright: ignore[reportMissingImports]
from app.alerta_popup import emitir_popup # pyright: ignore[reportMissingImports]

load_dotenv()

SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"
def carregar_empresas_monitoradas():
    try:
        resposta = supabase.table("empresas").select("nome").eq("monitorar", True).execute()
        return [linha["nome"] for linha in resposta.data]
    except Exception as e:
        print(f"⚠️ Erro ao carregar empresas monitoradas: {e}")
        return []

def manchete_valida(manchete: str) -> bool:
    if not manchete or len(manchete.strip()) < 10:
        return False
    blacklist = ["...", "sem título", "unknown", "http", "imagem"]
    return not any(p in manchete.lower() for p in blacklist)

def alerta_ja_existente(manchete: str) -> bool:
    try:
        resultado = supabase.table("alertas").select("noticia").eq("noticia", manchete).execute()
        return bool(resultado.data)
    except:
        return False

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

def classificar_risco(sentimento: str) -> str:
    if sentimento == "negativo":
        return "ALTO"
    elif sentimento == "neutro":
        return "MODERADO"
    else:
        return "BAIXO"

def gerar_frase_ia(sentimento: str, empresa: str) -> str: # pyright: ignore[reportReturnType]
    if sentimento == "negativo":
        return f"Atenção: notícias preocupantes sobre {empresa}. Recomendamos análise imediata."
    def monitorar_noticias():
        empresas = carregar_empresas_monitoradas()
        manchetes = buscar_manchetes_por_api(empresas)
        print("📡 Monitoramento iniciado...\n")

        for noticia in manchetes:
            if not manchete_valida(noticia):
                print(f"🚫 Manchete inválida: {noticia}")
                continue

            if alerta_ja_existente(noticia):
                print(f"🔁 Alerta já registrado: {noticia}")
                continue

            sentimento = analisar_sentimento(noticia)
            risco = classificar_risco(sentimento)
            empresa_encontrada = next((e for e in empresas if e.lower() in noticia.lower()), "Desconhecida")
            frase_ia = gerar_frase_ia(sentimento, empresa_encontrada)

            emitir_popup(frase_ia)
            enviar_alerta_email(empresa_encontrada, noticia, risco, sentimento)

            supabase.table("alertas").insert({
                "empresa": empresa_encontrada,
                "noticia": noticia,
                "sentimento": sentimento,
                "risco": risco,
                "frase_ia": frase_ia,
                "timestamp": datetime.now().isoformat()
            }).execute()

            print(f"✅ Alerta registrado: {noticia}\n🧠 Sentimento: {sentimento} | ⚠️ Risco: {risco}\n")