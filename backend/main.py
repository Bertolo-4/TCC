from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ConexaoBanco.conexao import get_connection
from Modelos.usuario import usuario
from Persistencia.usuarioDAO import inserir_usuario, buscar_usuario

app = Flask(__name__)
CORS(app)  # Permite chamadas de JS de qualquer origem

# Rota para servir arquivos estáticos (CSS, imagens)
@app.route('/frontend/<path:path>')
def send_static(path):
    return send_from_directory('frontend', path)

# Rota para criar usuário
@app.route('/criar-usuario', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios.'})

    u = usuario(nome=nome, email=email, senha=senha)
    u = inserir_usuario(u)

    if u.id_usuario is None:
        return jsonify({'success': False, 'message': f'Erro: email {email} já existe.'})

    return jsonify({'success': True, 'message': 'Usuário criado com sucesso!', 'id': u.id_usuario})

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios.'})

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nome, email, senha FROM usuario WHERE email=%s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result:
        return jsonify({'success': False, 'message': 'Email não encontrado.'})

    id_usuario, nome_usuario, email_usuario, senha_usuario = result
    if senha != senha_usuario:
        return jsonify({'success': False, 'message': 'Senha incorreta.'})

    return jsonify({'success': True, 'message': 'Login realizado com sucesso!', 'id': id_usuario, 'nome': nome_usuario})

if __name__ == "__main__":
    app.run(debug=True)
