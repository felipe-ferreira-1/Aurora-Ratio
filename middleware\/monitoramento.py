import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from utils.logger import log_info, log_warning
from datetime import datetime

# 🔍 Middleware que rastreia IP, token e ação
class RequisicaoMonitor(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        inicio = time.time()

        ip = request.client.host
        caminho = request.url.path
        token = request.headers.get("x-token", "sem token")

        log_info(f"Requisição recebida — IP: {ip} | Token: {token} | Caminho: {caminho}")

        # 🚨 Alerta automático para Game Master se detectar ação suspeita
        if "admin" in caminho or "ceo" in caminho:
            log_warning(f"🔐 Rota sensível acessada — {caminho} | IP: {ip} | Token: {token}")

        resposta = await call_next(request)
        fim = time.time()
        duracao = fim - inicio

        log_info(f"✔️ Requisição finalizada — {caminho} | Tempo: {duracao:.2f}s")
        return resposta