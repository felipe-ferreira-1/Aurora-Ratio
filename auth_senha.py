from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
router = APIRouter()
SECRET = os.getenv("JWT_SECRET", "aurora-default-secret")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
pwd_context = CryptContext(schemes=["argon2"])

# 📦 Modelos
class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioCadastro(BaseModel):
    email: str
    senha: str
    plano: str = "mensal"

# 🔒 Hash
def hash_senha(senha):
    return pwd_context.hash(senha)

def verificar_senha(senha, hash):
    return pwd_context.verify(senha, hash)

# 🎫 JWT
def gerar_token(email):
    return jwt.encode({"email": email}, SECRET, algorithm="HS256")

# ✅ Cadastro
@router.post("/auth/cadastrar")
def cadastrar(dados: UsuarioCadastro):
    senha_hash = hash_senha(dados.senha)
    try:
        supabase.table("usuarios").insert({
            "email": dados.email,
            "senha_hash": senha_hash,
            "plano": dados.plano,
            "ativo": True,
            "token": gerar_token(dados.email),
            "cargo": "usuario"
        }).execute()
        return {"msg": "Usuário cadastrado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔑 Login
@router.post("/auth/login")
def login(dados: UsuarioLogin):
    resposta = supabase.table("usuarios").select("*").eq("email", dados.email).single().execute().data
    if not resposta or not verificar_senha(dados.senha, resposta.get("senha_hash", "")):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"token": gerar_token(dados.email), "cargo": resposta["cargo"], "email": dados.email}
    from utils.email_helper import enviar_boas_vindas
    enviar_boas_vindas(dados.email)
    nova_senha = gerar_nova_senha()
    enviar_recuperacao(email, nova_senha)
    import random
    import string
    from utils.email_helper import enviar_recuperacao

    def gerar_nova_senha(tamanho=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))

    @router.post("/auth/recuperar")
    def recuperar_senha(dados: UsuarioLogin):
        # 🔍 Verifica se o email existe
        resposta = supabase.table("usuarios").select("*").eq("email", dados.email).single().execute().data
        if not resposta:
            raise HTTPException(status_code=404, detail="Email não encontrado")

        nova_senha = gerar_nova_senha()
        nova_hash = hash_senha(nova_senha)

        # 🛠️ Atualiza senha no banco
        try:
            supabase.table("usuarios").update({"senha_hash": nova_hash}).eq("email", dados.email).execute()
            enviar_recuperacao(dados.email, nova_senha)
            return {"msg": "Nova senha enviada por e-mail"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            from starlette.requests import Request
            @router.post("/auth/recuperar")
            async def recuperar_senha(dados: UsuarioLogin, request: Request):
                ip = request.client.host

                # 🔍 Busca registros de tentativas recentes
                auditoria = supabase.table("auditoria")\
                    .select("*").eq("ip", ip)\
                    .eq("acao", "recuperar")\
                    .order("timestamp", desc=True)\
                    .limit(1).execute().data

                if auditoria:
                    ultima = pd.to_datetime(auditoria[0]["timestamp"])
                    tempo = (datetime.utcnow() - ultima).total_seconds()
                    if tempo < 60:  # mínimo 60s entre tentativas
                        raise HTTPException(status_code=429, detail="Aguarde antes de tentar novamente")

                resposta = supabase.table("usuarios").select("*").eq("email", dados.email).single().execute().data
                if not resposta:
                    raise HTTPException(status_code=404, detail="Email não encontrado")

                nova_senha = gerar_nova_senha()
                nova_hash = hash_senha(nova_senha)

                try:
                    supabase.table("usuarios").update({"senha_hash": nova_hash}).eq("email", dados.email).execute()
                    enviar_recuperacao(dados.email, nova_senha)

                    # 🔐 Registrar na auditoria
                    supabase.table("auditoria").insert({
                        "email": dados.email,
                        "acao": "recuperar",
                        "ip": ip,
                        "cargo": resposta.get("cargo", "indefinido")
                    }).execute()

                    return {"msg": "Nova senha enviada por e-mail"}
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))