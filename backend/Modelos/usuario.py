class usuario:
    def __init__(self, nome, email, senha, id_usuario=None):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
