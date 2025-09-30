# Importe as bibliotecas necessárias
from fastapi import FastAPI
from pydantic import BaseModel  # Importe BaseModel para criar modelos de dados
import openai

# --- CONFIGURAÇÃO ---
# COLOQUE SUA CHAVE SECRETA DA OPENAI AQUI
# Exemplo: "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
openai.api_key = ""
app = FastAPI(
    title="API de Assistência ao Aluno",
    version="1.0"
)

# --- MODELOS DE DADOS DE ENTRADA (Request Body) ---
# Isso diz ao FastAPI para esperar um JSON no corpo da requisição.
# É a maneira padrão e mais organizada de fazer isso.
class AdaptarRequest(BaseModel):
    texto: str
    dificuldades: str
    facilidades: str

class CorrigirRequest(BaseModel):
    codigo: str
    dificuldades: str
    facilidades: str

# ========================
# Função: adaptar enunciado
# ========================
# (Sua função original, sem alterações na lógica)
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

    # ATENÇÃO: Sintaxe ATUALIZADA para a biblioteca openai v1.x+
    resposta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um especialista em simplificação de textos para fácil compreensão."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return resposta.choices[0].message.content

# =====================
# Função: corrigir código
# =====================
# (Sua função original, sem alterações na lógica)
def corrigir_codigo(codigo: str, dificuldades: str, facilidades: str):
    prompt = f"""
O aluno enviou o seguinte código como resposta. Corrija erros de sintaxe e lógica,
explique de forma simples o que foi corrigido, e adapte a explicação conforme o perfil do aluno.

Perfil do aluno:
- Dificuldades: {dificuldades}
- Facilidades: {facilidades}

Código do aluno:
\"\"\"{codigo}\"\"\"

Responda com:
1. Código corrigido.
2. Explicação em linguagem simples do que mudou.
"""

    # ATENÇÃO: Sintaxe ATUALIZADA para a biblioteca openai v1.x+
    resposta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um tutor de programação paciente e didático."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return resposta.choices[0].message.content

# ==========================
# Rotas da API
# ==========================
# Agora, a função recebe o objeto 'request' do tipo AdaptarRequest
@app.post("/adaptar-exercicio/")
def api_adaptar_exercicio(request: AdaptarRequest):
    resultado = adaptar_exercicio(request.texto, request.dificuldades, request.facilidades)
    return {"exercicio_adaptado": resultado}

# E aqui, recebe o objeto 'request' do tipo CorrigirRequest
@app.post("/corrigir-codigo/")
def api_corrigir_codigo(request: CorrigirRequest):
    resultado = corrigir_codigo(request.codigo, request.dificuldades, request.facilidades)
    return {"correcao": resultado}

@app.get("/")
def home():
    return "API está no ar. Vá para /docs para testar."