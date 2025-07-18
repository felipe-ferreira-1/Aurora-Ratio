from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABELAS = ["usuarios", "alertas", "empresas", "log_requisicoes"]
DIR_BACKUP = "backups"

os.makedirs(DIR_BACKUP, exist_ok=True)

def backup_tabela(tabela):
    try:
        dados = supabase.table(tabela).select("*").execute().data
        filename = f"{DIR_BACKUP}/{tabela}_{datetime.utcnow().strftime('%Y-%m-%d_%H-%M')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"✅ Backup salvo: {filename}")
    except Exception as e:
        print(f"❌ Erro ao fazer backup da tabela {tabela}: {e}")

def executar_backup():
    for tabela in TABELAS:
        backup_tabela(tabela)

if __name__ == "__main__":
    executar_backup()