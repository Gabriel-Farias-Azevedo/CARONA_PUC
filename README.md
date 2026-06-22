# 🚗 Caronas PUC-Rio

Plataforma web que conecta estudantes da PUC-Rio que **oferecem** e **procuram**
caronas até a universidade — mais econômico, prático e colaborativo.

Projeto da disciplina **Engenharia de Software** (Trabalho 2). Implementado em
**Python + Flask**, aplicando **Clean Architecture**, os princípios **SOLID** e
testes unitários com **Pytest**.

---

## Histórias de usuário implementadas

1. Como estudante, quero **me cadastrar com e-mail `@aluno.puc-rio.br`** para acessar a plataforma.
2. Como motorista, quero **oferecer uma carona** (origem, destino, data/hora, vagas e valor).
3. Como passageiro, quero **buscar caronas disponíveis** e **reservar uma vaga**.
4. Como passageiro, quero **cancelar uma reserva** e liberar a vaga.

Entidades de domínio: **User**, **Ride** (carona) e **Reservation** (reserva).

Regras de negócio garantidas pelo sistema:

- Cadastro restrito ao domínio **`@aluno.puc-rio.br`** (escopo do produto).
- Você **não reserva a sua própria** carona nem reserva a mesma carona duas vezes.
- **Sem overbooking**: a vaga é ocupada de forma atômica no banco; cancelar libera a vaga.
- Só aparecem caronas **futuras e com vaga**.

---

## Como rodar

Pré-requisito: **Python 3.10+**.

```bash
cd app-caronas
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac (descomente esta linha e comente a anterior)

pip install -r requirements.txt
python run.py
```

Abra **http://localhost:8000**. O banco SQLite é criado sozinho em
`storage/caronas.sqlite` na primeira execução.

### Rodar os testes

```bash
pytest -v
```

---

## Arquitetura — Clean Architecture

```
app-caronas/
├── domain/                 # Entidades (regras de negócio puras, sem dependências externas)
│   ├── user.py
│   ├── ride.py
│   └── reservation.py
│
├── use_cases/               # Casos de uso (regras de aplicação) + interfaces (portas)
│   ├── repositories.py        # Interfaces: UserRepository, RideRepository, ReservationRepository, TransactionManager
│   ├── exceptions.py           # ValidationError
│   ├── register_user.py
│   ├── offer_ride.py
│   ├── list_available_rides.py
│   ├── reserve_ride.py
│   └── cancel_reservation.py
│
├── infra/                   # Frameworks e Ferramentas Externas: implementação concreta com SQLite
│   ├── db/
│   │   ├── database.py        # conexão + criação do schema
│   │   └── transaction.py     # SqliteTransactionManager
│   └── repositories/
│       ├── sqlite_user_repository.py
│       ├── sqlite_ride_repository.py
│       └── sqlite_reservation_repository.py
│
├── app/                     # Adaptadores de Interface: Flask (rotas, templates, sessão, CSRF)
│   ├── __init__.py            # fábrica de aplicação + raiz de composição
│   ├── container.py           # liga interfaces (use_cases) às implementações (infra)
│   ├── auth.py                 # sessão / usuário autenticado / decorator login_required
│   ├── csrf.py                  # proteção CSRF baseada em sessão
│   ├── template_filters.py      # formatação de data e moeda para as views
│   ├── constants.py
│   ├── routes/                  # blueprints (1 por área: home, auth, rides, reservations, profile)
│   └── templates/               # views Jinja2
│
├── database/schema.sql       # esquema do banco (SQLite)
├── tests/
│   ├── domain/                  # testes das entidades
│   └── use_cases/                # testes dos use cases com repositórios fake (sem infraestrutura)
├── run.py                     # ponto de entrada
└── requirements.txt
```

### Fluxo de uma requisição

```
Navegador
   │  HTTP
   ▼
app/routes/*  ........... Blueprint Flask: traduz HTTP → chamada de use case
   ▼
use_cases/*  ............. regra de negócio (1 classe por caso de uso, método execute())
   ▼
use_cases/repositories.py  contrato de persistência (interface)  ← Inversão de Dependência
   ▼
infra/repositories/*  .... implementação concreta (SQLite)
   ▼
app/templates/*  ......... renderiza HTML (Jinja2)
```

### Onde cada princípio aparece no código

| Princípio / Padrão | Onde, no código |
|---|---|
| **Clean Architecture** | `domain/` (entidades) → `use_cases/` (regras de aplicação + interfaces) → `infra/` e `app/` (detalhes externos: banco, Flask) |
| **Responsabilidade Única (S)** | Cada use case (`RegisterUserUseCase`, `ReserveRideUseCase`, ...) tem um único motivo para mudar |
| **Aberto/Fechado (O)** | Novo banco de dados = novo `infra/repositories/*`, sem tocar nos use cases |
| **Substituição de Liskov (L)** | Qualquer implementação de `UserRepository`/`RideRepository`/`ReservationRepository` (SQLite ou fake de teste) pode substituir a outra sem quebrar o use case |
| **Segregação de Interface (I)** | Uma interface por agregado (`UserRepository`, `RideRepository`, `ReservationRepository`), não um repositório genérico único |
| **Inversão de Dependência (D)** | Use cases dependem das interfaces em `use_cases/repositories.py`; `app/container.py` injeta a implementação concreta SQLite |

### Segurança

- Senhas com `werkzeug.security.generate_password_hash` (nunca em texto puro).
- **Prepared statements** (parâmetros `?`) em toda query — anti-SQL injection.
- **Escape automático** de saída pelo Jinja2 — anti-XSS.
- **Token CSRF** validado em todo `POST`.
- Verificação de **posse** antes de cancelar uma reserva.

---

## Testes

Os testes em `tests/use_cases/` validam a lógica de negócio isolada da
infraestrutura, usando repositórios fake em memória (`tests/use_cases/fakes.py`)
que implementam as mesmas interfaces dos adaptadores SQLite reais.

```bash
pytest -v
```

---

## Equipe (Scrum)

- **Dono do Produto:** Lúcio · **Mestre Scrum:** Kalline · **Desenvolvedores:** Gabriel e Felipe
