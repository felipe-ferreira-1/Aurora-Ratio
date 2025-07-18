from fastapi import FastAPI
from app.routes import router
from middleware.monitoramento import RequisicaoMonitor
import uvicorn

# 👑 Inicialização do Império Aurora Ratio
app = FastAPI(
    title="Aurora Ratio API",
    description="Radar estratégico de notícias e inteligência de investimentos",
    version="1.0.0"
)

# 🛡️ Muralha ativa com rastreio de requisições
app.add_middleware(RequisicaoMonitor)

# 📦 Todas as rotas imperiais
app.include_router(router)

# 🚀 Execução local
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    from app.comentarios import router as comentarios_router
    app.include_router(comentarios_router)
    from app.cadastro import router as cadastro_router
    app.include_router(cadastro_router)