
import zipfile
import os

def compactar_com_senha(arquivo_original):
    senha = os.getenv("ZIP_SENHA", "aurora-default")
    zip_nome = arquivo_original.replace(".json", ".zip")

    try:
        with zipfile.ZipFile(zip_nome, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.setpassword(senha.encode("utf-8"))
            zf.write(arquivo_original, os.path.basename(arquivo_original))
        os.remove(arquivo_original)  # 🔥 Remove o original sem criptografia
        print(f"🔐 Arquivo criptografado: {zip_nome}")
    except Exception as e:
        print(f"❌ Erro ao compactar {arquivo_original}: {e}")

