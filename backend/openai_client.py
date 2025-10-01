import os
import time
from openai import OpenAI

_api_key = os.getenv("OPENAI_API_KEY")
if not _api_key:
    raise RuntimeError(
        "OPENAI_API_KEY não definido. Defina a variável de ambiente antes de executar (ex: setx OPENAI_API_KEY \"sua_chave\")."
    )

client = OpenAI(api_key=_api_key)

def explain_exercise(exercise_text: str, max_retries: int = 3) -> str:
    """
    Chama a API do OpenAI para gerar uma explicação. Faz retries simples em caso de falha.
    Retorna a explicação como string.
    """
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que explica exercícios de forma clara e simples."},
                    {"role": "user", "content": f"Explique este exercício de forma simples e passo a passo:\n\n{exercise_text}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            # seguros: diferentes SDKs podem retornar estrutura ligeiramente distinta
            choice = response.choices[0]
            # pode ser choice.message.content ou choice.text dependendo da versão
            content = getattr(choice, "message", None)
            if content:
                explanation = content.content.strip()
            else:
                explanation = (getattr(choice, "text", "") or "").strip()
            return explanation
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                backoff = 2 ** (attempt - 1)
                time.sleep(backoff)
            else:
                raise Exception(f"Erro ao chamar a API do OpenAI após {max_retries} tentativas: {e}") from e
