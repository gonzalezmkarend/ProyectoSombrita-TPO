# Pruebas de la lógica de src/menu_estadisticas.py.

from src.menu_estadisticas import (
    _calcular_ocupacion,
    _carpas_libres,
    _carpas_ocupadas,
    _cliente_con_mas_reservas,
    _contar_reservas_cliente,
    _dnis_con_reservas,
)

JUAN = 30111222
MARIA = 28333444


def test_carpas_ocupadas_devuelve_conjunto(reservas):
    """Dos reservas de la misma carpa cuentan como una sola carpa ocupada."""
    assert _carpas_ocupadas(reservas, "01/01/2027", "31/12/2027") == {1}


def test_carpas_ocupadas_sin_coincidencias(reservas):
    """Ninguna reserva cae en el rango."""
    assert _carpas_ocupadas(reservas, "01/06/2027", "02/06/2027") == set()


def test_carpas_libres_excluye_ocupadas_e_inactivas(carpas, reservas):
    """La 1 está ocupada y la 3 está inactiva: solo queda la 2."""
    assert _carpas_libres(carpas, reservas, "20/01/2027", "21/01/2027") == [2]


def test_carpas_libres_ordenadas():
    """Devuelve los números de menor a mayor."""
    assert _carpas_libres({5: True, 1: True, 3: True}, [], "01/01/2027", "02/01/2027") == [1, 3, 5]


def test_carpas_libres_sin_carpas(reservas):
    """Colección vacía."""
    assert _carpas_libres({}, reservas, "01/01/2027", "02/01/2027") == []


def test_ocupacion_parcial(carpas, reservas):
    """Una de las dos carpas activas está ocupada: 50 %."""
    assert _calcular_ocupacion(carpas, reservas, "20/01/2027", "21/01/2027") == 50.0


def test_ocupacion_sin_reservas_en_rango(carpas, reservas):
    """Ninguna carpa ocupada: 0 %."""
    assert _calcular_ocupacion(carpas, reservas, "01/06/2027", "02/06/2027") == 0.0


def test_ocupacion_total(reservas):
    """Todas las carpas activas ocupadas: 100 %."""
    assert _calcular_ocupacion({1: True}, reservas, "20/01/2027", "21/01/2027") == 100.0


def test_ocupacion_sin_carpas_activas(reservas):
    """Colección vacía: no debe dividir por cero."""
    assert _calcular_ocupacion({}, reservas, "01/01/2027", "02/01/2027") == 0.0
    assert _calcular_ocupacion({9: False}, reservas, "01/01/2027", "02/01/2027") == 0.0


def test_ocupacion_ignora_carpas_inactivas():
    """Una reserva sobre una carpa inactiva no cuenta para el porcentaje."""
    reservas_inactiva = [{"carpa": 9, "dni": JUAN, "desde": "01/01/2027", "hasta": "02/01/2027",
                          "estado": "reservada"}]
    carpas_prueba = {1: True, 9: False}
    assert _calcular_ocupacion(carpas_prueba, reservas_inactiva, "01/01/2027", "02/01/2027") == 0.0


def test_dnis_con_reservas(reservas):
    """Devuelve DNI distintos, sin repetir."""
    assert _dnis_con_reservas(reservas + reservas) == {JUAN, MARIA}


def test_contar_reservas_cliente(reservas):
    """Cuenta por DNI; un DNI sin reservas tiene 0."""
    assert _contar_reservas_cliente(reservas + reservas, JUAN) == 2
    assert _contar_reservas_cliente(reservas, 1) == 0


def test_cliente_con_mas_reservas(reservas):
    """Caso normal: Juan tiene dos reservas y María una."""
    extra = {"carpa": 2, "dni": JUAN, "desde": "01/01/2027", "hasta": "02/01/2027",
             "estado": "reservada"}
    assert _cliente_con_mas_reservas(reservas + [extra]) == JUAN


def test_cliente_con_mas_reservas_empate(reservas):
    """Límite: con una reserva cada uno, gana el DNI menor."""
    assert _cliente_con_mas_reservas(reservas) == MARIA


def test_cliente_con_mas_reservas_sin_reservas():
    """Colección vacía."""
    assert _cliente_con_mas_reservas([]) is None
