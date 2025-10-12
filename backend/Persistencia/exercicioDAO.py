from ConexaoBanco.conexao import get_connection
from Modelos.exercicio import exercicio
import mysql.connector

def inserir_exercicio(novo_exercicio):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO exercicio (titulo, enunciado, linguagem) VALUES (%s, %s, %s)"
        cursor.execute(sql, (novo_exercicio.titulo, novo_exercicio.enunciado, novo_exercicio.linguagem))

        conn.commit()
        novo_exercicio.id_exercicio = cursor.lastrowid

        cursor.close()
        return novo_exercicio
    except mysql.connector.Error as error:
        if conn:
            conn.rollback()
        print("Erro ao inserir exercício:", error)
        novo_exercicio.id_exercicio = None
        return novo_exercicio
    finally:
        if conn:
            conn.close()


def buscar_exercicio_por_id(id_exercicio):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_exercicio, titulo, enunciado, linguagem FROM exercicio WHERE id_exercicio=%s", (id_exercicio,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return exercicio(id_exercicio=result[0], titulo=result[1], enuciado=result[2], linguagem=result[3])
        return None
    except mysql.connector.Error as error:
        print("Erro ao buscar exercício:", error)
        return None
    finally:
        if conn:
            conn.close()
