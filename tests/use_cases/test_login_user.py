import pytest

from tests.use_cases.fakes import FakeUserRepository
from use_cases.exceptions import ValidationError
from use_cases.login_user import LoginUserUseCase
from use_cases.register_user import RegisterUserUseCase


def test_logs_in_with_correct_credentials():
    users = FakeUserRepository()
    RegisterUserUseCase(users).execute("Maria Clara", "maria@aluno.puc-rio.br", "senha123")

    user = LoginUserUseCase(users).execute("maria@aluno.puc-rio.br", "senha123")

    assert user.email == "maria@aluno.puc-rio.br"


def test_rejects_wrong_password():
    users = FakeUserRepository()
    RegisterUserUseCase(users).execute("Maria Clara", "maria@aluno.puc-rio.br", "senha123")

    with pytest.raises(ValidationError):
        LoginUserUseCase(users).execute("maria@aluno.puc-rio.br", "senhaerrada")


def test_rejects_unknown_email():
    with pytest.raises(ValidationError):
        LoginUserUseCase(FakeUserRepository()).execute("ninguem@aluno.puc-rio.br", "senha123")
