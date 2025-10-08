# Persistencia/perfilAlunoDAO.py

from ConexaoBanco.conexao import get_connection
from Modelos.perfilAluno import perfilAluno

# Nota: Não precisamos mais importar o psycopg2 aqui
# Se o seu conector for o mysql-connector-python, você pode importá-lo para tratar erros
import mysql.connector

def inserir_usuario(Aluno):
    """
    Insere um novo usuário no banco de dados MySQL e retorna o objeto com o ID.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # SQL de inserção simples, SEM o RETURNING
        sql = "INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)"
        
        cursor.execute(sql, (Aluno.dificuldades, Aluno.facilidades))
        
        # Salva (commita) as alterações
        conn.commit()
        
        # No MySQL, usamos cursor.lastrowid para pegar o ID do último item inserido
        Aluno.id_perfil = cursor.lastrowid
        
        cursor.close()
        return Aluno
    except mysql.connector.Error as error:
        if conn:
            conn.rollback() # Desfaz a transação em caso de erro
        print("Erro ao inserir preferencias:", error)
        Aluno.id_perfil = None
        return Aluno
    finally:
        if conn:
            conn.close()
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nome, email, senha FROM Usuario WHERE email=%s",
            (email,)
        )
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return perfilAluno(id_perfil==result[0], dificuldades==result[1], facilidades==result[2])
        
        return None
    except mysql.connector.Error as error:
        print("Erro ao buscar usuário:", error)
        return None
    finally:
        if conn:
            conn.close()
