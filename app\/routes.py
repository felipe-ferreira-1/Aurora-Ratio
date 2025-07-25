from fastapi import APIRouter, HTTPException, Depends, Header
from app.sentiment import analisar_sentimento
from app.auth import validar_token, usuario_por_token, verificar_cargo
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🏢 EMPRESAS MONITORADAS
@router.get("/empresas/")
def listar_empresas(x_token: str = Depends(validar_token)):
    try:
        resposta = supabase.table("empresas").select("*").eq("monitorar", True).execute()
        return resposta.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar empresas: {e}")

# 📡 ANALISAR MANCHETE
@router.get("/analisar/")
def analisar_noticia(noticia: str, x_token: str = Depends(validar_token)):
    if not noticia or len(noticia.strip()) < 5:
        raise HTTPException(status_code=400, detail="Notícia inválida")
    resultado = analisar_sentimento(noticia)
    return {"noticia": noticia, "sentimento": resultado
    from app.auth_senha import router as auth_router
    app.include_router(auth_router)