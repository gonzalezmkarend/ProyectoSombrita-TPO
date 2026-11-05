# Pruebas de la lógica de src/menu_carpas.py.

from src.menu_carpas import (
    _cambiar_estado_carpa,
    _listar_carpas,
    _modificar_carpa,
    _registrar_carpa,
)


def test_registrar_carpa_nueva(carpas):
    """Caso normal: queda registrada y activa."""
    assert _registrar_carpa(carpas, 4) is True
    assert carpas[4] is True


def test_registrar_carpa_numero_no_positivo(carpas):
    """Dato inválido: 0 y negativos no se registran."""
    assert _registrar_carpa(carpas, 0) is False
    assert _registrar_carpa(carpas, -1) is False
    assert carpas == {1: True, 2: True, 3: False}


def test_registrar_carpa_repetida(carpas):
    """Regla del negocio: el número es único. Tampoco cambia el estado de la existente."""
    assert _registrar_carpa(carpas, 3) is False
    assert carpas[3] is False


def test_modificar_carpa_actualiza_sus_reservas(carpas, reservas):
    """Regla del negocio: las reservas siguen apuntando a la carpa renombrada."""
    assert _modificar_carpa(carpas, reservas, 1, 9) is True
    assert 1 not in carpas and carpas[9] is True
    assert [reserva["carpa"] for reserva in reservas] == [9, 9]


def test_modificar_carpa_conserva_estado(carpas, reservas):
    """Una carpa inactiva sigue inactiva con el número nuevo."""
    assert _modificar_carpa(carpas, reservas, 3, 9) is True
    assert carpas[9] is False


def test_modificar_carpa_inexistente(carpas, reservas):
    """Búsqueda sin resultado."""
    assert _modificar_carpa(carpas, reservas, 99, 9) is False


def test_modificar_carpa_numero_en_uso(carpas, reservas):
    """Regla del negocio: el número nuevo no puede estar en uso. No modifica nada."""
    assert _modificar_carpa(carpas, reservas, 1, 2) is False
    assert carpas == {1: True, 2: True, 3: False}
    assert [reserva["carpa"] for reserva in reservas] == [1, 1]


def test_modificar_carpa_numero_invalido(carpas, reservas):
    """Dato inválido: el número nuevo debe ser mayor a 0."""
    assert _modificar_carpa(carpas, reservas, 1, 0) is False


def test_inactivar_carpa_sin_reservas(carpas, reservas):
    """Borrado lógico: la carpa sigue existiendo, inactiva."""
    assert _cambiar_estado_carpa(carpas, reservas, 2, False) is True
    assert carpas[2] is False


def test_inactivar_carpa_con_reservas(carpas, reservas):
    """Regla del negocio: no se puede inactivar una carpa con reservas."""
    assert _cambiar_estado_carpa(carpas, reservas, 1, False) is False
    assert carpas[1] is True


def test_activar_carpa(carpas, reservas):
    """Una carpa inactiva vuelve a estar activa."""
    assert _cambiar_estado_carpa(carpas, reservas, 3, True) is True
    assert carpas[3] is True


def test_cambiar_estado_carpa_inexistente(carpas, reservas):
    """Búsqueda sin resultado: no crea la carpa."""
    assert _cambiar_estado_carpa(carpas, reservas, 99, True) is False
    assert 99 not in carpas


def test_listar_carpas_ordenadas():
    """Ordena por número aunque se hayan cargado desordenadas."""
    assert _listar_carpas({5: True, 1: False, 3: True}) == [(1, False), (3, True), (5, True)]


def test_listar_carpas_solo_activas(carpas):
    """Excluye las inactivas."""
    assert _listar_carpas(carpas, solo_activas=True) == [(1, True), (2, True)]


def test_listar_carpas_vacio():
    """Colección vacía."""
    assert _listar_carpas({}) == []
