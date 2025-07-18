from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
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