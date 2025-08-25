from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

# Importando as classes e funções dos outros arquivos do projeto
from Modelos.usuario import usuario as ModeloUsuario
from Persistencia.usuarioDAO import inserir_usuario, buscar_usuario

# --- Modelos de Dados (Pydantic) para validação automática ---

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class GenericResponse(BaseModel):
    success: bool
    message: str

class UserCreatedResponse(GenericResponse):
    id: int

class LoginSuccessResponse(GenericResponse):
    id: int
    nome: str

# --- Aplicação FastAPI ---

app = FastAPI()

# --- Middleware de CORS ---
# Permite que o frontend (rodando em outra porta) acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para o domínio do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints da API ---

@app.post("/criar-usuario", response_model=UserCreatedResponse, status_code=status.HTTP_201_CREATED, responses={409: {"model": GenericResponse}})
async def criar_usuario_api(user_data: UsuarioCreate):
    """
    Cria um novo usuário, verificando antes se o e-mail já existe.
    """
    # 1. Verifica se o usuário já existe usando a função da DAO
    usuario_existente = buscar_usuario(user_data.email)
    if usuario_existente:
        # 2. Se existir, retorna um erro 409 Conflict (Conflito)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Erro: email {user_data.email} já existe.'
        )
        
    # 3. Se não existir, cria o novo objeto e chama a função de inserção
    novo_usuario = ModeloUsuario(nome=user_data.nome, email=user_data.email, senha=user_data.senha)
    usuario_criado = inserir_usuario(novo_usuario)

    # 4. Verifica se a inserção no banco deu certo
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

@app.post("/login", response_model=LoginSuccessResponse, responses={404: {"model": GenericResponse}, 401: {"model": GenericResponse}})
async def login_api(login_data: UsuarioLogin):
    """
    Autentica um usuário.
    """
    # Utiliza a função buscar_usuario para manter a lógica de banco na DAO
    usuario_encontrado = buscar_usuario(login_data.email)
    
    if not usuario_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email não encontrado."
        )
    
    # IMPORTANTE: Em produção, nunca compare senhas em texto puro!
    # Use uma biblioteca como passlib para criar e verificar hashes de senha.
    if login_data.senha != usuario_encontrado.senha:
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

# --- Servir Arquivos Estáticos ---
# Monta a pasta 'frontend' para ser acessível via URL '/frontend'
app.mount("/frontend", StaticFiles(directory="../frontend"), name="static")
