from domain.user import User
from tests.use_cases.fakes import FakeUserRepository
from use_cases.update_profile import UpdateProfileUseCase


def test_updates_name_course_and_phone():
    users = FakeUserRepository()
    user = users.save(User(id=None, name="Maria", email="maria@aluno.puc-rio.br", password_hash="hash"))

    updated = UpdateProfileUseCase(users).execute(user, "Maria Clara", "Engenharia", "21", "98888-7777")

    assert updated.name == "Maria Clara"
    assert updated.course == "Engenharia"
    assert updated.phone == "21988887777"
    assert users.find_by_id(user.id).name == "Maria Clara"


def test_keeps_email_unchanged_and_clears_empty_phone():
    users = FakeUserRepository()
    user = users.save(User(id=None, name="Maria", email="maria@aluno.puc-rio.br", password_hash="hash"))

    updated = UpdateProfileUseCase(users).execute(user, "Maria Clara", "", "", "")

    assert updated.email == "maria@aluno.puc-rio.br"
    assert updated.phone is None
