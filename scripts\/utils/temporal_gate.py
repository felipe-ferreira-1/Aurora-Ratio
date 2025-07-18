import base64
import json

def gerar_portao_temporal(email, cargo_simulado):
    payload = {"email": email, "cargo": cargo_simulado}
    texto = json.dumps(payload)
    token = base64.urlsafe_b64encode(texto.encode()).decode()
    return f"TEMP:{token}"