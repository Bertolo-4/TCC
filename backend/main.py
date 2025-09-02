from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# Importando as classes e funções dos outros arquivos do projeto
from Modelos.usuario import usuario as ModeloUsuario
from Persistencia.usuarioDAO import inserir_usuario, buscar_usuario

# --- Contexto de Hashing de Senha ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Funções de Hashing ---
def verify_password(plain_password, hashed_password):
    return  pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- Endpoints da API ---


# Esta é a rota para a página inicial que estava faltando.
@app.get("/", response_model=GenericResponse)
async def raiz_api():
    return {
        "success": True, 
        "message": "API está online e funcionando!"
    }

@app.post("/criar-usuario", response_model=UserCreatedResponse, status_code=status.HTTP_201_CREATED, responses={409: {"model": GenericResponse}})
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

@app.post("/login", response_model=LoginSuccessResponse, responses={404: {"model": GenericResponse}, 401: {"model": GenericResponse}})
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

# --- Servir Arquivos Estáticos ---
app.mount("/frontend", StaticFiles(directory="../frontend"), name="static")
