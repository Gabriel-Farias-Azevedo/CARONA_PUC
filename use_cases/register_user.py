import re

from werkzeug.security import generate_password_hash

from domain.user import User
from use_cases.exceptions import ValidationError
from use_cases.repositories import UserRepository

ALLOWED_EMAIL_DOMAIN = "@aluno.puc-rio.br"
MIN_PASSWORD_LENGTH = 6
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RegisterUserUseCase:
    """Cadastra um novo estudante. Restrito a e-mails @aluno.puc-rio.br --
    regra de negócio central do produto (escopo: comunidade PUC-Rio).
    """

    def __init__(self, users: UserRepository):
        self._users = users

    def execute(
        self,
        name: str,
        email: str,
        password: str,
        course: str = "",
        ddd: str = "",
        phone: str = "",
    ) -> User:
        name = name.strip()
        email = email.strip().lower()
        course = course.strip()

        clean_phone = re.sub(r"\D", "", phone.strip())
        clean_ddd = re.sub(r"\D", "", ddd.strip())
        full_phone = clean_ddd + clean_phone if clean_ddd and clean_phone else ""

        errors: list[str] = []
        if name == "":
            errors.append("Informe o seu nome.")
        if not EMAIL_PATTERN.match(email):
            errors.append("Informe um e-mail válido.")
        if not email.endswith(ALLOWED_EMAIL_DOMAIN):
            errors.append(f"O e-mail deve ser um endereço válido {ALLOWED_EMAIL_DOMAIN}")
        if len(password) < MIN_PASSWORD_LENGTH:
            errors.append(f"A senha deve ter ao menos {MIN_PASSWORD_LENGTH} caracteres.")
        if ddd.strip() != "" and phone.strip() == "":
            errors.append("Se informar o DDD, informe também o número do telefone.")

        if errors:
            raise ValidationError(errors)

        if self._users.find_by_email(email) is not None:
            raise ValidationError(["Já existe uma conta com este e-mail."])

        user = User(
            id=None,
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            course=course or None,
            phone=full_phone or None,
        )
        return self._users.save(user)
