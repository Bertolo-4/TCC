from ConexaoBanco.conexao import get_connection
from Modelos.perfilAluno import perfilAluno
import mysql.connector

def inserir_perfil_aluno(novo_perfil):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO perfil_aluno (id_usuario, dificuldades, facilidades) VALUES (%s, %s, %s)"
        cursor.execute(sql, (novo_perfil.id_usuario, novo_perfil.dificuldades, novo_perfil.facilidades))

        conn.commit()
        novo_perfil.id_perfil = cursor.lastrowid

        cursor.close()
        return novo_perfil
    except mysql.connector.Error as error:
        if conn:
            conn.rollback()
        print("Erro ao inserir perfil_aluno:", error)
        novo_perfil.id_perfil = None
        return novo_perfil
    finally:
        if conn:
            conn.close()


def buscar_perfil_por_usuario(id_usuario):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(buffered=True)  # <-- adicionado buffered
        cursor.execute("SELECT id_perfil, id_usuario, dificuldades, facilidades FROM perfil_aluno WHERE id_usuario=%s", (id_usuario,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return perfilAluno(id_perfil=result[0], id_usuario=result[1], dificuldades=result[2], facilidades=result[3])
        return None
    except mysql.connector.Error as error:
        print("Erro ao buscar perfil:", error)
        return None
    finally:
        if conn:
            conn.close()

