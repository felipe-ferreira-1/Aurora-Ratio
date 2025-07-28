import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from fastapi import Header, HTTPException # pyright: ignore[reportMissingImports]
from supabase import create_client # pyright: ignore[reportMissingImports]

# 🔐 Carrega variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🧱 Verifica se o token enviado é válido
def validar_token(x_token: str = Header(...)):
    if not AUTH_TOKEN:
        raise HTTPException(status_code=500, detail="Token do servidor não configurado")
    if x_token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return x_token

# 🧑‍💼 Verifica se o token corresponde a usuário específico
def usuario_por_token(x_token: str = Header(...)):
    try:
        resposta = supabase.table("usuarios").select("*").eq("token", x_token).single().execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return resposta.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao validar token do usuário: {e}")

# 👑 Verifica se o cargo do usuário está entre os permitidos
def verificar_cargo(cargos_permitidos: list, x_token: str = Header(...)):
    try:
        usuario = supabase.table("usuarios").select("cargo").eq("token", x_token).single().execute().data
        if not usuario or usuario["cargo"] not in cargos_permitidos:
            raise HTTPException(status_code=403, detail="Acesso não autorizado para esse cargo")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar cargo: {e}")