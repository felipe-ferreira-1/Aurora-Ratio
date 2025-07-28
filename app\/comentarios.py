from fastapi import APIRouter, HTTPException # pyright: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]
from supabase import create_client # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
import os

load_dotenv()
router = APIRouter()

SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Comentario(BaseModel):
    alerta_id: str
    autor_email: str
    mensagem: str
    resposta_a: str | None = None # pyright: ignore[reportGeneralTypeIssues]

@router.post("/comentario")
def comentar(dados: Comentario):
    try:
        supabase.table("comentarios_alerta").insert({
            "alerta_id": dados.alerta_id,
            "autor_email": dados.autor_email,
            "mensagem": dados.mensagem,
            "resposta_a": dados.resposta_a
        }).execute()
        return {"msg": "Comentário registrado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))