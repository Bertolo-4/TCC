from ConexaoBanco.conexao import get_connection
from Modelos.codigo_resposta import codigo_resposta
import mysql.connector

def inserir_codigo_resposta(nova_resposta):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO codigo_resposta (id_usuario, id_exercicio, codigo_submetido, codigo_corrigido, feedback)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nova_resposta.id_usuario, nova_resposta.id_exercicio,
                             nova_resposta.codigo_submetido, nova_resposta.codigo_corrigido, None))

        conn.commit()
        nova_resposta.id_resposta = cursor.lastrowid

        cursor.close()
        return nova_resposta
    except mysql.connector.Error as error:
        if conn:
            conn.rollback()
        print("Erro ao inserir código_resposta:", error)
        nova_resposta.id_resposta = None
        return nova_resposta
    finally:
        if conn:
            conn.close()


def buscar_respostas_por_usuario(id_usuario):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_resposta, id_usuario, id_exercicio, codigo_submetido, codigo_corrigido, feedback
            FROM codigo_resposta
            WHERE id_usuario=%s
        """, (id_usuario,))
        resultados = cursor.fetchall()
        cursor.close()

        respostas = []
        for r in resultados:
            respostas.append(codigo_resposta(
                id_resposta=r[0],
                id_usuario=r[1],
                id_exercicio=r[2],
                codigo_submetido=r[3],
                codigo_corrigido=r[4]
            ))
        return respostas
    except mysql.connector.Error as error:
        print("Erro ao buscar respostas:", error)
        return []
    finally:
        if conn:
            conn.close()
