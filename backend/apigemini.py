from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai

# =======================
# CONFIGURAÇÃO DO CLIENTE
# =======================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


MODEL_NAME = "gemini-2.5-flash"

app = FastAPI(
    title="API de Assistência ao Aluno (Gemini 2.5)",
    version="1.0"
)


class AdaptarRequest(BaseModel):
    texto: str
    dificuldades: str
    facilidades: str

class CorrigirRequest(BaseModel):
    codigo: str
    dificuldades: str
    facilidades: str


# ==========================
# FUNÇÃO: ADAPTAR EXERCÍCIO
# ==========================
def adaptar_exercicio(texto: str, dificuldades: str, facilidades: str):
    prompt = f"""
Você é um revisor especializado em Linguagem Simples, seguindo o Guia de Linguagem Simples do Incaper.

Reescreva o exercício abaixo aplicando as seguintes regras:
- Use palavras comuns e conhecidas.
- Evite jargões e termos técnicos (explique se precisar usar).
- Prefira verbos a substantivos.
- Frases curtas (até 25 palavras).
- Ordem direta: sujeito + verbo + complemento.
- Prefira voz ativa.
- Parágrafos curtos (uma ideia por parágrafo).
- Organize o texto de forma lógica.
- Se possível, use listas para informações em sequência.
- Mantenha o sentido original.

Adapte considerando o perfil do aluno:
- Dificuldades: {dificuldades}
- Facilidades: {facilidades}

Exercício original:
\"\"\"{texto}\"\"\"

Retorne apenas o exercício adaptado.
"""

    model = genai.GenerativeModel(MODEL_NAME)
    resposta = model.generate_content(prompt)

    return resposta.text.strip()


# ==========================
# FUNÇÃO: CORRIGIR CÓDIGO
# ==========================
def corrigir_codigo(codigo: str, dificuldades: str, facilidades: str):
    prompt = f"""
O aluno enviou o seguinte código como resposta. Corrija erros de sintaxe e lógica,
explique de forma simples o que foi corrigido e adapte a explicação conforme o perfil do aluno.

Perfil do aluno:
- Dificuldades: {dificuldades}
- Facilidades: {facilidades}

Código do aluno:
\"\"\"{codigo}\"\"\"

Responda com:
1. Código corrigido.
2. Explicação em linguagem simples do que mudou.
"""

    model = genai.GenerativeModel(MODEL_NAME)
    resposta = model.generate_content(prompt)

    return resposta.text.strip()


# ======================
# ROTAS DA API
# ======================
@app.post("/adaptar-exercicio/")
def api_adaptar_exercicio(request: AdaptarRequest):
    resultado = adaptar_exercicio(request.texto, request.dificuldades, request.facilidades)
    return {"exercicio_adaptado": resultado}


@app.post("/corrigir-codigo/")
def api_corrigir_codigo(request: CorrigirRequest):
    resultado = corrigir_codigo(request.codigo, request.dificuldades, request.facilidades)
    return {"correcao": resultado}


@app.get("/")
def home():
    return "API (Gemini 2.5) está no ar. Vá para /docs para testar."
