# Persistencia/usuarioDAO.py

from ConexaoBanco.conexao import get_connection
from Modelos.usuario import usuario
import mysql.connector

def inserir_usuario(novo_usuario):
    """
    Insere um novo usuário no banco de dados MySQL e retorna o objeto com o ID.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # SQL de inserção simples, SEM o RETURNING
        sql = "INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)"
        
        cursor.execute(sql, (novo_usuario.nome, novo_usuario.email, novo_usuario.senha))
        
        # Salva (commita) as alterações
        conn.commit()
        
        # No MySQL, usamos cursor.lastrowid para pegar o ID do último item inserido
        novo_usuario.id_usuario = cursor.lastrowid
        
        cursor.close()
        return novo_usuario
    except mysql.connector.Error as error:
        if conn:
            conn.rollback() # Desfaz a transação em caso de erro
        print("Erro ao inserir usuário:", error)
        novo_usuario.id_usuario = None
        return novo_usuario
    finally:
        if conn:
            conn.close()

# A função buscar_usuario não precisa de alterações, pois o SELECT é padrão
def buscar_usuario(email):
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nome, email, senha FROM Usuario WHERE email=%s",
            (email,)
        )
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return usuario(id_usuario=result[0], nome=result[1], email=result[2], senha=result[3])
        
        return None
    except mysql.connector.Error as error:
        print("Erro ao buscar usuário:", error)
        return None
    finally:
        if conn:
            conn.close()
