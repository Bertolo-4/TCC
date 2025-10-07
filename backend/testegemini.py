import requests

# URL base da API FastAPI com Gemini 2.5
BASE_URL = "http://127.0.0.1:8000"

print("=== Teste: /adaptar-exercicio/ (Gemini 2.5) ===")

with open("exercicios/exercicio1.txt", "r", encoding="utf-8") as f:
    texto = f.read().strip()
    
print(f"Exercício carregado do arquivo: {len(texto)} caracteres.")
dificuldades = input("Dificuldades do aluno: ")
facilidades = input("Facilidades do aluno: ")

# Corpo da requisição JSON
adaptar_payload = {
    "texto": texto,
    "dificuldades": dificuldades,
    "facilidades": facilidades
}


try:
    response = requests.post(f"{BASE_URL}/adaptar-exercicio/", json=adaptar_payload)
    
    print("\n=== Resultado ===")
    if response.status_code == 200:
        print(response.json().get("exercicio_adaptado", "Resposta inesperada."))
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Erro: Não foi possível conectar à API. Verifique se ela está rodando com 'uvicorn api_gemini:app --reload'.")
except Exception as e:
    print(f"❌ Ocorreu um erro inesperado: {e}")
