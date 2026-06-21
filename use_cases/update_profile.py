import re

from domain.user import User
from use_cases.repositories import UserRepository


class UpdateProfileUseCase:
    """Atualiza dados de perfil (nome, curso, telefone). O e-mail é a
    identidade do estudante e nunca é alterado por aqui.
    """

    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, user: User, name: str, course: str, ddd: str, phone: str) -> User:
        clean_ddd = re.sub(r"\D", "", ddd)
        clean_phone = re.sub(r"\D", "", phone)

        if clean_ddd and clean_phone:
            full_phone = clean_ddd + clean_phone
        elif clean_phone:
            full_phone = clean_phone
        else:
            full_phone = ""

        updated = User(
            id=user.id,
            name=name.strip() or user.name,
            email=user.email,
            password_hash=user.password_hash,
            course=course.strip() or None,
            phone=full_phone or None,
            created_at=user.created_at,
        )
        self._users.update(updated)
        return updated
