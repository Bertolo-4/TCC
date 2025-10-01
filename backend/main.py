from pathlib import Path
import warnings
import logging

# tentar import relativo, com fallback para import absoluto (útil ao rodar via uvicorn)
try:
    from .routes import router
except Exception:
    from routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Aplicação FastAPI ---
app = FastAPI(title="TCC Backend")

# --- Middleware de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router)

# --- Servir Arquivos Estáticos (caminho absoluto) ---
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_dir)), name="static")
    logger.info(f"Montado diretório estático: {frontend_dir}")
else:
    warnings.warn(f"Diretório estático não encontrado: {frontend_dir}. Rota /frontend não estará disponível.")
    logger.warning(f"Diretório estático não encontrado: {frontend_dir}")

@app.on_event("startup")
async def startup_event():
    logger.info("Aplicação iniciando. Vá para /docs para documentação interativa.")
