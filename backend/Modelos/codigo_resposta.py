class codigo_resposta:
    def __init__(self, codigo_submetido, codigo_corrigido, id_resposta=None, id_exercicio=None, id_usuario=None):
        self.id_resposta = id_resposta
        self.codigo_submetido = codigo_submetido
        self.codigo_corrigido = codigo_corrigido
        self.id_exercicio = id_exercicio
        self.id_usuario = id_usuario