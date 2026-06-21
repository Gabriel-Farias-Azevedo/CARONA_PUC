from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    """Estudante da plataforma. Pode atuar como motorista (ao oferecer caronas)
    ou passageiro (ao reservar) -- o papel é definido pela ação, não pelo cadastro.
    Entidade imutável: dados nunca mudam silenciosamente depois de criados.
    """

    id: Optional[int]
    name: str
    email: str
    password_hash: str
    course: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[str] = None

    def first_name(self) -> str:
        return self.name.strip().split(" ")[0]
