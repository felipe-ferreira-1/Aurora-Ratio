import logging
import os

# 🗂️ Criar diretório de logs se não existir
os.makedirs("logs", exist_ok=True)

# 🔧 Configuração básica
logging.basicConfig(
    filename="logs/aurora.log",
    format="%(asctime)s — %(levelname)s — %(message)s",
    level=logging.INFO
)

def log_info(msg):
    logging.info(msg)

def log_warning(msg):
    logging.warning(msg)

def log_error(msg):
    logging.error(msg)

def log_critical(msg):
    logging.critical(msg)
    from supabase import create_client
    import os
    from dotenv import load_dotenv
    from datetime import datetime

    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    def registrar_acao(email: str, acao: str, ip: str, cargo: str = "indefinido"):
        try:
            supabase.table("auditoria").insert({
                "email": email,
                "acao": acao,
                "ip": ip,
                "cargo": cargo,
                "timestamp": datetime.utcnow().isoformat()
            }).execute()
            print(f"📜 Auditoria registrada: {acao} | {email} | {ip}")
        except Exception as e:
            print(f"⚠️ Erro ao registrar auditoria: {e}")