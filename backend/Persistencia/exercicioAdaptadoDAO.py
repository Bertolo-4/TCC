from ConexaoBanco.conexao import get_connection
from Modelos.exercicioAdaptado import exercicioAdaptado
import mysql.connector

def inserir_exercicio_adaptado(novo_adaptado):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO exercicio_adaptado (id_usuario, id_exercicio, enunciado_adaptado) VALUES (%s, %s, %s)"
        cursor.execute(sql, (novo_adaptado.id_usuario, novo_adaptado.id_exercicio, novo_adaptado.enunciado_adaptado))

        conn.commit()
        novo_adaptado.id_adaptado = cursor.lastrowid

        cursor.close()
        return novo_adaptado
    except mysql.connector.Error as error:
        if conn:
            conn.rollback()
        print("Erro ao inserir exercício adaptado:", error)
        novo_adaptado.id_adaptado = None
        return novo_adaptado
    finally:
        if conn:
            conn.close()


def buscar_adaptado_por_usuario_e_exercicio(id_usuario, id_exercicio):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_adaptado, id_usuario, id_exercicio, enunciado_adaptado
            FROM exercicio_adaptado
            WHERE id_usuario=%s AND id_exercicio=%s
        """, (id_usuario, id_exercicio))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return exercicioAdaptado(id_adaptado=result[0], id_usuario=result[1], id_exercicio=result[2], enunnciado_adaptado=result[3])
        return None
    except mysql.connector.Error as error:
        print("Erro ao buscar exercício adaptado:", error)
        return None
    finally:
        if conn:
            conn.close()
