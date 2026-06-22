from domain.user import User


def test_first_name_returns_only_first_word():
    user = User(
        id=1,
        name="Maria Clara Souza",
        email="maria@aluno.puc-rio.br",
        password_hash="hash",
    )
    assert user.first_name() == "Maria"


def test_first_name_strips_surrounding_whitespace():
    user = User(
        id=1, name="  João Silva  ", email="joao@aluno.puc-rio.br", password_hash="hash"
    )
    assert user.first_name() == "João"
