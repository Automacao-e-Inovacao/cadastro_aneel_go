class ErroPrevisto(Exception):
    def __init__(self, mensagem, valor=None):
        self.mensagem = mensagem
        self.valor = valor
        super().__init__(self.mensagem)
