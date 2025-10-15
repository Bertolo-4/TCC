import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Importa os ROTEADORES de outros arquivos ---
from rotasExercicio import router as exercicios_router
from Routers.autenticacao import router as auth_router 

# --- Cria a instância principal da aplicação ---
app = FastAPI(
    title="API SimpleCode",
    description="API principal que gerencia exercícios e usuários."
)

# --- Adiciona Middlewares ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUI OS ROTEADORES NA APLICAÇÃO PRINCIPAL ---

# Adiciona as rotas de autenticação (ex: /auth/login)
app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])

# Adiciona as rotas de exercícios (ex: /api/exercicio/{id})
app.include_router(exercicios_router, prefix="/api", tags=["Exercícios"])


# --- Rota Raiz ---
@app.get("/", tags=["Status"])
async def raiz_api():
    return {"message": "Bem-vindo à API SimpleCode! Acesse /docs para a documentação."}


# --- Servir Arquivos Estáticos (Frontend) ---
# Esta linha deve vir por último
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
