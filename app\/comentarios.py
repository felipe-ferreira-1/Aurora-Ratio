from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Comentario(BaseModel):
    alerta_id: str
    autor_email: str
    mensagem: str
    resposta_a: str | None = None

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