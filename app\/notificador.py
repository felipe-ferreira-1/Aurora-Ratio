import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

def enviar_alerta_email(empresa, noticia, sentimento):
    assunto = f"[RadarAlpha] Alerta: {empresa} → {sentimento}"
    corpo = f"""
    🏢 Empresa: {empresa}
    📰 Notícia: {noticia}
    💬 Sentimento: {sentimento}
    """

    msg = EmailMessage()
    msg.set_content(corpo)
    msg["Subject"] = assunto
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(ratioaurora@gmail.com, aurorafeliperatio) # pyright: ignore[reportUndefinedVariable]
            smtp.send_message(msg)
            print("📩 Alerta enviado por e-mail com sucesso!")
    except Exception as e:
        print(f"⚠️ Falha no envio de e-mail: {e}")