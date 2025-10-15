from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# Importe seus modelos e DAOs
# ATENÇÃO: Verifique se os caminhos de importação estão corretos
# Pode ser necessário ajustar dependendo de como você executa a aplicação
from Modelos.usuario import usuario as ModeloUsuario
from Persistencia.usuarioDAO import inserir_usuario, buscar_usuario

# --- Crie uma instância do Roteador ---
router = APIRouter()

# --- Copie toda a lógica que estava no main.py para cá ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- Endpoints (ROTAS) ---

@router.post("/criar-usuario", summary="Cria um novo usuário")
async def criar_usuario_api(user_data: UsuarioCreate):
    usuario_existente = buscar_usuario(user_data.email)
    if usuario_existente:
        raise HTTPException(status_code=409, detail=f'Erro: email {user_data.email} já existe.')
    
    hashed_password = get_password_hash(user_data.senha)
    novo_usuario = ModeloUsuario(nome=user_data.nome, email=user_data.email, senha=hashed_password)
    usuario_criado = inserir_usuario(novo_usuario)
    
    if not usuario_criado or not usuario_criado.id_usuario:
        raise HTTPException(status_code=500, detail="Erro ao criar o usuário.")
        
    return {"success": True, "message": "Usuário criado com sucesso!", "id": usuario_criado.id_usuario}

@router.post("/login", summary="Realiza a autenticação do usuário")
async def login_api(login_data: UsuarioLogin):
    usuario_encontrado = buscar_usuario(login_data.email)
    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Email não encontrado.")
        
    if not verify_password(login_data.senha, usuario_encontrado.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta.")
        

    return {"success": True, "message": "Login realizado!", "id": usuario_encontrado.id_usuario, "nome": usuario_encontrado.nome}