from ConexaoBanco.conexao import get_connection
from Modelos.usuario import usuario

def inserir_usuario(usuario):
    conn = get_connection()
    cursor = conn.cursor()

    # verifica se email já existe
    cursor.execute("SELECT id_usuario, nome, email, senha FROM Usuario WHERE email=%s", (usuario.email,))
    result = cursor.fetchone()
    if result:
        usuario.id_usuario = result[0]
        usuario.nome = result[1]
        usuario.email = result[2]
        usuario.senha = result[3]
        cursor.close()
        conn.close()
        return usuario

    # insere novo usuário
    cursor.execute(
        "INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)",
        (usuario.nome, usuario.email, usuario.senha)
    )
    conn.commit()
    usuario.id_usuario = cursor.lastrowid
    cursor.close()
    conn.close()
    return usuario

def buscar_usuario(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_usuario, nome, email, senha FROM Usuario WHERE email=%s",
        (email,)
    )
    r = cursor.fetchone()
    cursor.close()
    conn.close()
    if r:
        return usuario(*r)  # id_usuario, nome, email, senha
    return None
