from werkzeug.security import check_password_hash

from domain.user import User
from use_cases.exceptions import ValidationError
from use_cases.repositories import UserRepository


class LoginUserUseCase:
    """Autentica um estudante já cadastrado por e-mail e senha."""

    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, email: str, password: str) -> User:
        user = self._users.find_by_email(email.strip().lower())

        if user is None or not check_password_hash(user.password_hash, password):
            raise ValidationError(["E-mail ou senha inválidos."])

        return user
