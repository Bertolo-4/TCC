from pydantic import BaseModel, EmailStr

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

class ExerciseExplainRequest(BaseModel):
    exercise_text: str

class ExerciseExplainResponse(BaseModel):
    explanation: str
