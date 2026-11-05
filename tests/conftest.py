# Datos y ayudas compartidas por todas las pruebas.
# pytest carga este archivo solo; cada fixture se recibe como parámetro de la prueba.

import pytest


@pytest.fixture
def carpas() -> dict[int, bool]:
    """Carpas de prueba: la 1 y la 2 activas, la 3 inactiva. Se crean de nuevo en cada prueba."""
    return {1: True, 2: True, 3: False}


@pytest.fixture
def clientes() -> dict[int, dict]:
    """Dos clientes de prueba."""
    return {
        30111222: {"nombre": "Juan Pérez", "telefono": "11-5555-1111"},
        28333444: {"nombre": "María Gómez", "telefono": "11 5555 2222"},
    }


@pytest.fixture
def reservas() -> list[dict]:
    """Dos reservas de prueba sobre la carpa 1, en enero y febrero de 2027."""
    return [
        {"carpa": 1, "dni": 30111222, "desde": "01/02/2027", "hasta": "14/02/2027",
         "estado": "alquilada"},
        {"carpa": 1, "dni": 28333444, "desde": "15/01/2027", "hasta": "31/01/2027",
         "estado": "reservada"},
    ]


@pytest.fixture
def simular_teclado(monkeypatch):
    """Reemplaza input() para que devuelva, en orden, las respuestas indicadas."""
    def _configurar(respuestas: list[str]) -> None:
        pendientes = iter(respuestas)
        monkeypatch.setattr("builtins.input", lambda mensaje="": next(pendientes))
    return _configurar
