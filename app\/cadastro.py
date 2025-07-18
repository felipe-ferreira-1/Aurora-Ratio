from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class NovoUsuario(BaseModel):
    email: str
    plano: str  # mensal ou anual
    pais: str
    moeda_preferida: str
    lang: str

@router.post("/cadastro")
def cadastrar(usuario: NovoUsuario):
    try:
        # 🔐 Geração de token simples (futuramente JWT ou com expiração)
        from uuid import uuid4
        token = str(uuid4())

        # 📦 Inserir novo usuário
        supabase.table("usuarios").insert({
            "email": usuario.email,
            "plano": usuario.plano,
            "pais": usuario.pais,
            "moeda_preferida": usuario.moeda_preferida,
            "lang": usuario.lang,
            "token": token,
            "cargo": "usuario"
🧠👑 Bem-vindo ao Império Aurora Ratio!

Olá [NOME_DO_USUÁRIO],

É uma honra tê-lo entre os estrategistas do Aurora Ratio — a plataforma que une inteligência de mercado, visão preditiva e colaboração estratégica.

Seu acesso foi ativado com sucesso.  
🔐 Token de entrada: [SEU_TOKEN]  
🌐 Idioma preferido: [LANG]  
🪙 Moeda de referência: [MOEDA]

Recomendamos iniciar explorando:
- Seus alertas personalizados
- A área de comentários VIP (se aplicável)
- As análises da IA preditiva de mercado

Se precisar de suporte, nossa IA está sempre ao seu lado.

O futuro já começou.  
Bem-vindo à muralha da inteligência.

Atenciosamente,  
Equipe Aurora Ratio