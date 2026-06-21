class ValidationError(Exception):
    """Erro para dados inválidos ou regra de negócio violada (ex.: 'não há mais
    vagas'). Carrega uma lista de mensagens, permitindo que as rotas tratem
    todos os erros de forma uniforme (DRY).
    """

    def __init__(self, errors: list[str]):
        super().__init__(" ".join(errors))
        self.errors = errors

    def as_text(self) -> str:
        return " ".join(self.errors)
