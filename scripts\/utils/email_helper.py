import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")  # Ex: aurora@gmail.com
EMAIL_SENHA = os.getenv("EMAIL_SENHA")          # Senha do app no Gmail

yag = yagmail.SMTP(EMAIL_REMETENTE, EMAIL_SENHA)

def enviar_boas_vindas(destinatario):
    try:
        yag.send(
            to=destinatario,
            subject="🌟 Bem-vindo ao Aurora Ratio",
            contents="Você foi registrado com sucesso no império. Prepare-se para investir com inteligência!"
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def enviar_alerta_gamemaster(email_suspeito, rota, ip):
    try:
        yag.send(
            to=EMAIL_REMETENTE,
            subject="🚨 Alerta de acesso suspeito",
            contents=f"Atenção Game Master:\n\nUsuário {email_suspeito} acessou {rota} via IP {ip}.\nVerifique imediatamente."
        )
        return True
    except:
        return False

def enviar_recuperacao(email, nova_senha):
    try:
        yag.send(
            to=email,
            subject="🔐 Recuperação de acesso",
            contents=f"Sua nova senha provisória é: {nova_senha}\nAltere assim que possível."
        )
        return True
    except Exception as e:
        print(e)
        return False