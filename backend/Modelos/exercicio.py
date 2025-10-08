class exercicio: 
    def __init__(self, titulo, enuciado, linguagem, id_exercicio=None):
        self.id_exercicio = id_exercicio
        self.titulo = titulo
        self.enunciado = enuciado
        self.linguagem = linguagem