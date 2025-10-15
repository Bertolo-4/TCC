# routers/exercicios.py
from fastapi import APIRouter, HTTPException, status

from Persistencia.exercicioDAO import ExercicioDAO
from apigemini import adaptar_exercicio_para_iniciante

router = APIRouter()
exercicio_dao = ExercicioDAO()

@router.get("/exercicio/{exercicio_id}", summary="Obtém um exercício adaptado (com cache)")
def get_exercicio_com_cache(exercicio_id: int):
    exercicio = exercicio_dao.buscar_por_id(exercicio_id)
    if not exercicio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercício não encontrado")

    # MUDANÇA AQUI: Verificamos a chave "enunciado_adaptado"
    if exercicio.get("enunciado_adaptado"):
        print(f"Servindo exercício {exercicio_id} do cache do banco de dados.")
        # MUDANÇA AQUI: Retornamos o valor de "enunciado_adaptado"
        return {"enunciado_adaptado": exercicio["enunciado_adaptado"]}

    try:
        print(f"Adaptando exercício {exercicio_id} com a API Gemini...")
        
        # MUDANÇA AQUI: Passamos o valor da chave "enunciado" para a IA
        texto_adaptado = adaptar_exercicio_para_iniciante(exercicio["enunciado"])
        
        exercicio_dao.salvar_versao_adaptada(exercicio_id, texto_adaptado)
        
        # MUDANÇA AQUI: Retornamos o resultado na chave "enunciado_adaptado"
        return {"enunciado_adaptado": texto_adaptado}
    except Exception as e:
        print(f"Erro na lógica de adaptação: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adaptar o exercício.")