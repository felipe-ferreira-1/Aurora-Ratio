from fastapi import APIRouter, HTTPException, Request # pyright: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]
from datetime import datetime
from supabase import create_client # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
import os

load_dotenv()
router = APIRouter()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class PagamentoRequest(BaseModel):
    email: str
    plano: str  # mensal ou anual
    metodo: str  # stripe, picpay, mercado

@router.post("/pagamento/simular")
def simular_pagamento(dados: PagamentoRequest):
    valor = 50 if dados.plano == "mensal" else 500
    try:
        supabase.table("auditoria").insert({
            "email": dados.email,
            "acao": f"pagamento-{dados.metodo}",
            "ip": "localhost",
            "cargo": "usuario"
        }).execute()
        supabase.table("usuarios").update({"plano": dados.plano, "ativo": True}).eq("email", dados.email).execute()
        return {
            "msg": f"Plano {dados.plano.upper()} ativado com sucesso",
            "valor": f"R${valor},00",
            "metodo": dados.metodo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))