from fastapi import APIRouter, HTTPException, status
from Modelos.usuario import usuario as ModeloUsuario
from Persistencia.usuarioDAO import inserir_usuario, buscar_usuario
from .models import UsuarioCreate, UsuarioLogin, GenericResponse, UserCreatedResponse, LoginSuccessResponse, ExerciseExplainRequest, ExerciseExplainResponse
from .auth import verify_password, get_password_hash
from .openai_client import explain_exercise
import asyncio

router = APIRouter()

# --- Endpoints da API ---
@router.get("/", response_model=GenericResponse)
async def raiz_api():
    return {
        "success": True,
        "message": "API está online e funcionando!"
    }

@router.post("/criar-usuario", response_model=UserCreatedResponse, status_code=status.HTTP_201_CREATED, responses={409: {"model": GenericResponse}})
async def criar_usuario_api(user_data: UsuarioCreate):
    usuario_existente = buscar_usuario(user_data.email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Erro: email {user_data.email} já existe.'
        )

    hashed_password = get_password_hash(user_data.senha)
    novo_usuario = ModeloUsuario(nome=user_data.nome, email=user_data.email, senha=hashed_password)

    usuario_criado = inserir_usuario(novo_usuario)

    if not usuario_criado or not usuario_criado.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao criar o usuário."
        )

    return {
        "success": True,
        "message": "Usuário criado com sucesso!",
        "id": usuario_criado.id_usuario
    }

@router.post("/login", response_model=LoginSuccessResponse, responses={404: {"model": GenericResponse}, 401: {"model": GenericResponse}})
async def login_api(login_data: UsuarioLogin):
    usuario_encontrado = buscar_usuario(login_data.email)

    if not usuario_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email não encontrado."
        )

    if not verify_password(login_data.senha, usuario_encontrado.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta."
        )

    return {
        "success": True,
        "message": "Login realizado com sucesso!",
        "id": usuario_encontrado.id_usuario,
        "nome": usuario_encontrado.nome
    }

@router.post("/explain-exercise", response_model=ExerciseExplainResponse, responses={500: {"model": GenericResponse}})
async def explain_exercise_api(request: ExerciseExplainRequest):
    try:
        # executar a chamada bloqueante em um thread para não bloquear o loop async
        explanation = await asyncio.to_thread(explain_exercise, request.exercise_text)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao explicar o exercício: {str(e)}"
        )
