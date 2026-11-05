# Pruebas de la lógica de clientes y reservas de src/menu_reservas.py.

import pytest

from src.menu_reservas import (
    _buscar_cliente_por_nombre,
    _buscar_reserva,
    _buscar_reservas_por_texto,
    _cambiar_estado_reserva,
    _cancelar_reserva,
    _consultar_reservas_cliente,
    _leer_fecha_del_dia,
    _normalizar_nombre,
    _ordenar_reservas,
    _registrar_cliente,
    _registrar_reserva,
    _reservas_del_dia,
    _validar_telefono,
)

JUAN = 30111222
MARIA = 28333444


# --- Clientes ---

def test_normalizar_nombre():
    """Quita espacios sobrantes y capitaliza, incluso con tildes."""
    assert _normalizar_nombre("  juan   PÉREZ ") == "Juan Pérez"


@pytest.mark.parametrize("telefono", ["11-5555-1111", "+54 11 5555 3333", "123456"])
def test_validar_telefono_valido(telefono):
    """Formatos aceptados; 6 dígitos es el mínimo."""
    assert _validar_telefono(telefono) is True


@pytest.mark.parametrize("telefono", ["11-ABC-1111", "12345", ""])
def test_validar_telefono_invalido(telefono):
    """Dato inválido: letras, menos de 6 dígitos o vacío."""
    assert _validar_telefono(telefono) is False


def test_registrar_cliente_normaliza(clientes):
    """Caso normal: guarda el nombre normalizado."""
    assert _registrar_cliente(clientes, 1234, " ana  ruiz ", " 11-5555-3333 ") is True
    assert clientes[1234] == {"nombre": "Ana Ruiz", "telefono": "11-5555-3333"}


def test_registrar_cliente_dni_repetido(clientes):
    """Regla del negocio: el DNI es único y no se pisan los datos existentes."""
    assert _registrar_cliente(clientes, JUAN, "Otro", "11-5555-3333") is False
    assert clientes[JUAN]["nombre"] == "Juan Pérez"


@pytest.mark.parametrize("dni, nombre, telefono", [
    (0, "Ana", "11-5555-3333"),
    (1234, "   ", "11-5555-3333"),
    (1234, "Ana", "sin teléfono"),
])
def test_registrar_cliente_datos_invalidos(clientes, dni, nombre, telefono):
    """Dato inválido: DNI, nombre o teléfono. No agrega nada."""
    assert _registrar_cliente(clientes, dni, nombre, telefono) is False
    assert len(clientes) == 2


def test_buscar_cliente_por_nombre_sin_mayusculas(clientes):
    """Búsqueda exitosa por parte del nombre, sin distinguir mayúsculas."""
    assert _buscar_cliente_por_nombre(clientes, "PÉR") == [JUAN]


def test_buscar_cliente_por_nombre_sin_resultado(clientes):
    """Búsqueda sin resultado."""
    assert _buscar_cliente_por_nombre(clientes, "Zzz") == []


# --- Registrar reserva ---

def test_registrar_reserva_valida(carpas, clientes, reservas):
    """Caso normal."""
    assert _registrar_reserva(reservas, carpas, clientes, 2, JUAN,
                              "01/01/2027", "15/01/2027", "alquilada") is True
    assert reservas[-1] == {"carpa": 2, "dni": JUAN, "desde": "01/01/2027",
                            "hasta": "15/01/2027", "estado": "alquilada"}


def test_registrar_reserva_de_un_dia(carpas, clientes, reservas):
    """Límite: desde y hasta pueden ser el mismo día."""
    assert _registrar_reserva(reservas, carpas, clientes, 2, JUAN,
                              "01/01/2027", "01/01/2027") is True


def test_registrar_reserva_estado_por_defecto(carpas, clientes, reservas):
    """Sin indicar estado, queda como reservada."""
    _registrar_reserva(reservas, carpas, clientes, 2, JUAN, "01/01/2027", "02/01/2027")
    assert reservas[-1]["estado"] == "reservada"


@pytest.mark.parametrize("carpa, dni, desde, hasta, estado", [
    (3, JUAN, "01/01/2027", "02/01/2027", "reservada"),    # carpa inactiva
    (99, JUAN, "01/01/2027", "02/01/2027", "reservada"),   # carpa inexistente
    (2, 1, "01/01/2027", "02/01/2027", "reservada"),       # cliente inexistente
    (2, JUAN, "31/04/2027", "02/05/2027", "reservada"),    # fecha desde inválida
    (2, JUAN, "01/01/2027", "32/01/2027", "reservada"),    # fecha hasta inválida
    (2, JUAN, "10/01/2027", "01/01/2027", "reservada"),    # desde posterior a hasta
    (2, JUAN, "01/01/2027", "02/01/2027", "pagada"),       # estado inexistente
    (1, JUAN, "20/01/2027", "25/01/2027", "reservada"),    # carpa ocupada
    (1, JUAN, "10/01/2027", "15/01/2027", "reservada"),    # se toca en un día con otra
])
def test_registrar_reserva_rechazada(carpas, clientes, reservas, carpa, dni, desde, hasta, estado):
    """Regla del negocio o dato inválido: devuelve False y no agrega nada."""
    assert _registrar_reserva(reservas, carpas, clientes, carpa, dni, desde, hasta, estado) is False
    assert len(reservas) == 2


def test_registrar_reserva_contigua(carpas, clientes, reservas):
    """Límite: puede empezar el día siguiente a que termina otra reserva."""
    assert _registrar_reserva(reservas, carpas, clientes, 1, JUAN,
                              "15/02/2027", "20/02/2027") is True


def test_registrar_reserva_misma_fecha_otra_carpa(carpas, clientes, reservas):
    """La superposición solo importa dentro de la misma carpa."""
    assert _registrar_reserva(reservas, carpas, clientes, 2, JUAN,
                              "20/01/2027", "25/01/2027") is True


# --- Buscar, cancelar y cambiar estado ---

def test_buscar_reserva(reservas):
    """Búsqueda exitosa (devuelve el índice) y sin resultado (-1)."""
    assert _buscar_reserva(reservas, 1, MARIA, "15/01/2027") == 1
    assert _buscar_reserva(reservas, 1, MARIA, "16/01/2027") == -1


def test_cancelar_reserva(reservas):
    """Elimina solamente la reserva indicada."""
    assert _cancelar_reserva(reservas, 1, MARIA, "15/01/2027") is True
    assert len(reservas) == 1 and reservas[0]["dni"] == JUAN


def test_cancelar_primera_reserva(reservas):
    """Elimina la reserva buscada aunque no sea la última de la lista."""
    assert _cancelar_reserva(reservas, 1, JUAN, "01/02/2027") is True
    assert len(reservas) == 1 and reservas[0]["dni"] == MARIA


def test_cancelar_reserva_inexistente(reservas):
    """Búsqueda sin resultado: no elimina nada."""
    assert _cancelar_reserva(reservas, 2, MARIA, "15/01/2027") is False
    assert len(reservas) == 2


def test_cambiar_estado_a_alquilada(reservas):
    """Caso normal: se pagó la reserva."""
    assert _cambiar_estado_reserva(reservas, 1, MARIA, "15/01/2027", "alquilada") is True
    assert reservas[1]["estado"] == "alquilada"


def test_cambiar_estado_inexistente_o_invalido(reservas):
    """Reserva inexistente o estado inválido: no modifica nada."""
    assert _cambiar_estado_reserva(reservas, 2, MARIA, "15/01/2027", "alquilada") is False
    assert _cambiar_estado_reserva(reservas, 1, MARIA, "15/01/2027", "pagada") is False
    assert reservas[1]["estado"] == "reservada"


# --- Listados ---

def test_ordenar_por_fecha_real(reservas):
    """Enero va antes que febrero, aunque como texto "01/02" sea menor que "15/01"."""
    ordenadas = _ordenar_reservas(reservas, "fecha")
    assert [reserva["desde"] for reserva in ordenadas] == ["15/01/2027", "01/02/2027"]


def test_ordenar_por_carpa_sin_modificar_original():
    """Ordena por carpa y conserva la lista original."""
    originales = [{"carpa": 2, "desde": "01/01/2027"}, {"carpa": 1, "desde": "02/01/2027"}]
    ordenadas = _ordenar_reservas(originales, "carpa")
    assert [reserva["carpa"] for reserva in ordenadas] == [1, 2]
    assert originales[0]["carpa"] == 2


def test_ordenar_lista_vacia():
    """Colección vacía."""
    assert _ordenar_reservas([]) == []


def test_consultar_reservas_cliente(reservas):
    """Filtra por DNI; un DNI sin reservas devuelve una lista vacía."""
    assert len(_consultar_reservas_cliente(reservas, JUAN)) == 1
    assert _consultar_reservas_cliente(reservas, 1) == []


def test_buscar_reservas_por_dni(reservas, clientes):
    """Un texto de solo dígitos se busca como DNI."""
    encontradas = _buscar_reservas_por_texto(reservas, clientes, str(MARIA))
    assert [reserva["dni"] for reserva in encontradas] == [MARIA]


def test_buscar_reservas_por_nombre(reservas, clientes):
    """Cualquier otro texto se busca en el nombre, sin distinguir mayúsculas."""
    encontradas = _buscar_reservas_por_texto(reservas, clientes, "juan")
    assert [reserva["dni"] for reserva in encontradas] == [JUAN]


def test_buscar_reservas_sin_resultado(reservas, clientes):
    """Búsqueda sin resultado por nombre y por DNI."""
    assert _buscar_reservas_por_texto(reservas, clientes, "Zzz") == []
    assert _buscar_reservas_por_texto(reservas, clientes, "123") == []


@pytest.mark.parametrize("fecha, cantidad", [
    ("15/01/2027", 1),   # primer día de la reserva
    ("31/01/2027", 1),   # último día de la reserva
    ("20/01/2027", 1),   # día intermedio
    ("14/01/2027", 0),   # día anterior
    ("01/03/2027", 0),   # día sin reservas
])
def test_reservas_del_dia(reservas, fecha, cantidad):
    """Límite: los extremos del rango cuentan como vigentes."""
    assert len(_reservas_del_dia(reservas, fecha)) == cantidad


def test_leer_fecha_del_dia_hoy(simular_teclado, monkeypatch):
    """La opción Hoy devuelve la fecha actual sin pedir que se escriba."""
    monkeypatch.setattr("src.menu_reservas._fecha_de_hoy", lambda: "10/01/2027")
    simular_teclado(["1"])
    assert _leer_fecha_del_dia() == "10/01/2027"


def test_leer_fecha_del_dia_otra_fecha(simular_teclado):
    """La opción Otra fecha pide la fecha y rechaza una inexistente."""
    simular_teclado(["2", "31/04/2027", "20/01/2027"])
    assert _leer_fecha_del_dia() == "20/01/2027"


def test_leer_fecha_del_dia_opcion_invalida(simular_teclado, monkeypatch, capsys):
    """Una opción inexistente avisa y vuelve a preguntar."""
    monkeypatch.setattr("src.menu_reservas._fecha_de_hoy", lambda: "10/01/2027")
    simular_teclado(["3", "1"])
    assert _leer_fecha_del_dia() == "10/01/2027"
    assert "opción inválida" in capsys.readouterr().out
