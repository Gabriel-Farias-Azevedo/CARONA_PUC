import re
from datetime import datetime


def format_datetime_br(value: str) -> str:
    """Formata 'YYYY-MM-DD HH:MM' para o padrão brasileiro 'DD/MM/YYYY às HH:MM'."""
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return value
    return parsed.strftime("%d/%m/%Y às %H:%M")


def format_currency_brl(value: float) -> str:
    """Formata um valor numérico como moeda brasileira (R$ 1.234,56)."""
    formatted = f"{float(value):,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")
