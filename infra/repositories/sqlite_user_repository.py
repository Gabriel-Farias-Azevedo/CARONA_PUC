import sqlite3
from typing import Optional

from domain.user import User
from use_cases.repositories import UserRepository


class SqliteUserRepository(UserRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def find_by_email(self, email: str) -> Optional[User]:
        row = self._conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return self._hydrate(row) if row else None

    def find_by_id(self, user_id: int) -> Optional[User]:
        row = self._conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return self._hydrate(row) if row else None

    def save(self, user: User) -> User:
        cursor = self._conn.execute(
            "INSERT INTO users (name, email, password_hash, course, phone) VALUES (?, ?, ?, ?, ?)",
            (user.name, user.email, user.password_hash, user.course, user.phone),
        )
        return User(
            id=cursor.lastrowid,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            course=user.course,
            phone=user.phone,
        )

    def update(self, user: User) -> None:
        self._conn.execute(
            "UPDATE users SET name = ?, course = ?, phone = ? WHERE id = ?",
            (user.name, user.course, user.phone, user.id),
        )

    @staticmethod
    def _hydrate(row: sqlite3.Row) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            course=row["course"],
            phone=row["phone"],
            created_at=row["created_at"],
        )
