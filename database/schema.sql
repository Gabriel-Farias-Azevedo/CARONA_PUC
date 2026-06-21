-- Esquema do banco (SQLite). Idempotente: roda a cada boot sem efeito colateral.

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    course          TEXT, 
    phone           TEXT,
    created_at    TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS rides (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id      INTEGER NOT NULL REFERENCES users(id),
    origin         TEXT NOT NULL,
    destination    TEXT NOT NULL,
    departure_at   TEXT NOT NULL,
    seats_total    INTEGER NOT NULL,
    seats_taken    INTEGER NOT NULL DEFAULT 0,
    price_per_seat REAL NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS reservations (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ride_id      INTEGER NOT NULL REFERENCES rides(id),
    passenger_id INTEGER NOT NULL REFERENCES users(id),
    status       TEXT NOT NULL DEFAULT 'ativa',
    created_at   TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_rides_departure ON rides(departure_at);
CREATE INDEX IF NOT EXISTS idx_reservations_passenger ON reservations(passenger_id);
