# routers/exercicios.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from Persistencia.exercicioDAO import ExercicioDAO
from apigemini import adaptar_exercicio, corrigir_codigo

router = APIRouter()
exercicio_dao = ExercicioDAO()

# --- Modelos Pydantic ---
class ExercicioCreate(BaseModel):
    titulo: str
    enunciado: str
    linguagem: str = "Java"
    template_codigo: Optional[str] = None

class CodigoRequest(BaseModel):
    codigo: str # Garante que o nome do campo é 'codigo'

# --- Rotas ---
@router.get("/exercicios", summary="Lista todos os exercícios disponíveis")
def get_todos_exercicios():
    return exercicio_dao.listar_todos()

@router.post("/exercicios", summary="Cria um novo exercício")
def create_exercicio(exercicio_data: ExercicioCreate):
    novo_exercicio = exercicio_dao.inserir_exercicio(
        exercicio_data.titulo,
        exercicio_data.enunciado,
        exercicio_data.linguagem,
        exercicio_data.template_codigo
    )
    if not novo_exercicio:
        raise HTTPException(status_code=500, detail="Erro ao criar o exercício.")
    return novo_exercicio

@router.get("/exercicio/{exercicio_id}", summary="Obtém um exercício adaptado (com cache)")
def get_exercicio_com_cache(exercicio_id: int):
    exercicio = exercicio_dao.buscar_por_id(exercicio_id)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    if exercicio.get("enunciado_adaptado"):
        return exercicio
    
    try:
        texto_adaptado = adaptar_exercicio(exercicio["enunciado"], "", "")
        exercicio_dao.salvar_versao_adaptada(exercicio_id, texto_adaptado)
        exercicio["enunciado_adaptado"] = texto_adaptado
        return exercicio
    except Exception as e:
        raise HTTPException(status_code=500, detail="Falha ao adaptar o exercício.")


@router.post("/exercicio/{exercicio_id}/run-code", summary="Executa e corrige o código de um exercício")
def run_code(exercicio_id: int, request: CodigoRequest):
    exercicio = exercicio_dao.buscar_por_id(exercicio_id)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado para correção.")

    try:
        
        feedback_ia = corrigir_codigo(request.codigo, exercicio['enunciado'])
        
        # feedback_ia = corrigir_codigo(request.codigo)

        # Retorna na chave 'output' como o frontend espera
        return {"output": feedback_ia}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar código: {str(e)}")
