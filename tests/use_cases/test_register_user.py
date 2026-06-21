import pytest

from tests.use_cases.fakes import FakeUserRepository
from use_cases.exceptions import ValidationError
from use_cases.register_user import RegisterUserUseCase


def test_registers_user_with_valid_puc_email():
    use_case = RegisterUserUseCase(FakeUserRepository())

    user = use_case.execute("Maria Clara", "maria@aluno.puc-rio.br", "senha123")

    assert user.id is not None
    assert user.email == "maria@aluno.puc-rio.br"
    assert user.password_hash != "senha123"


def test_rejects_email_outside_puc_domain():
    use_case = RegisterUserUseCase(FakeUserRepository())

    with pytest.raises(ValidationError) as exc:
        use_case.execute("Maria Clara", "maria@gmail.com", "senha123")

    assert "@aluno.puc-rio.br" in exc.value.as_text()


def test_rejects_short_password():
    use_case = RegisterUserUseCase(FakeUserRepository())

    with pytest.raises(ValidationError):
        use_case.execute("Maria Clara", "maria@aluno.puc-rio.br", "123")


def test_rejects_duplicate_email():
    users = FakeUserRepository()
    use_case = RegisterUserUseCase(users)
    use_case.execute("Maria Clara", "maria@aluno.puc-rio.br", "senha123")

    with pytest.raises(ValidationError) as exc:
        use_case.execute("Outra Maria", "maria@aluno.puc-rio.br", "outrasenha")

    assert "Já existe uma conta" in exc.value.as_text()


def test_requires_phone_number_when_ddd_is_given_without_phone():
    use_case = RegisterUserUseCase(FakeUserRepository())

    with pytest.raises(ValidationError) as exc:
        use_case.execute("Maria Clara", "maria@aluno.puc-rio.br", "senha123", ddd="21")

    assert "DDD" in exc.value.as_text()
