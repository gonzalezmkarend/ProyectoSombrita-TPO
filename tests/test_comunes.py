# Pruebas de src/comunes.py: fechas, quicksort, consultas compartidas y lectura por teclado.

import pytest

from src.comunes import (
    ESTADO_LIBRE,
    _consultar_estado_carpa,
    _esta_ocupada,
    _fecha_de_hoy,
    _leer_entero,
    _leer_fecha,
    _leer_rango_fechas,
    _leer_texto,
    _nombre_cliente,
    _quicksort,
    _se_superponen,
    _validar_fecha,
)


# --- Fechas ---

def test_validar_fecha_valida():
    """Caso normal."""
    assert _validar_fecha("15/01/2027") is True


def test_fecha_de_hoy_es_valida():
    """Postcondición: el texto respeta el formato que usa el resto del programa."""
    assert _validar_fecha(_fecha_de_hoy()) is True


def test_validar_fecha_dia_inexistente():
    """Abril tiene 30 días."""
    assert _validar_fecha("31/04/2027") is False


def test_validar_fecha_29_febrero_bisiesto():
    """Límite: 2028 es bisiesto."""
    assert _validar_fecha("29/02/2028") is True


def test_validar_fecha_29_febrero_no_bisiesto():
    """Límite: 2027 no es bisiesto."""
    assert _validar_fecha("29/02/2027") is False


@pytest.mark.parametrize("fecha", ["1/1/2027", "2027-01-15", "01/13/2027", "", "abc"])
def test_validar_fecha_formatos_invalidos(fecha):
    """Dato inválido: no respeta dd/mm/aaaa. No debe lanzar una excepción."""
    assert _validar_fecha(fecha) is False


def test_se_superponen_rangos_separados():
    """Rangos sin días en común."""
    assert _se_superponen("01/01/2027", "10/01/2027", "11/01/2027", "20/01/2027") is False


def test_se_superponen_comparten_un_dia():
    """Límite: comparten solo el último día de uno y el primero del otro."""
    assert _se_superponen("01/01/2027", "10/01/2027", "10/01/2027", "20/01/2027") is True


def test_se_superponen_uno_dentro_del_otro():
    """Un rango contiene por completo al otro."""
    assert _se_superponen("01/01/2027", "31/01/2027", "10/01/2027", "12/01/2027") is True


def test_se_superponen_compara_fechas_y_no_texto():
    """Como texto "15/01" es mayor que "01/02", pero como fecha es anterior."""
    assert _se_superponen("15/01/2027", "20/01/2027", "01/02/2027", "05/02/2027") is False


# --- Quicksort ---

def test_quicksort_lista_vacia():
    """Colección vacía: caso base de la recursión."""
    assert _quicksort([], lambda valor: valor) == []


def test_quicksort_ordena_con_repetidos():
    """Caso normal con elementos repetidos."""
    assert _quicksort([3, 1, 2, 3, 0], lambda valor: valor) == [0, 1, 2, 3, 3]


def test_quicksort_usa_la_clave():
    """Ordena según la función clave, no por el elemento completo."""
    lista = [("b", 2), ("a", 3), ("c", 1)]
    assert _quicksort(lista, lambda par: par[1]) == [("c", 1), ("b", 2), ("a", 3)]


def test_quicksort_no_modifica_la_original():
    """Postcondición: devuelve una lista nueva."""
    original = [2, 1]
    _quicksort(original, lambda valor: valor)
    assert original == [2, 1]


def test_quicksort_conserva_orden_de_claves_iguales():
    """Postcondición: los elementos con la misma clave no se reordenan."""
    lista = [("a", 1), ("b", 0), ("c", 1)]
    assert _quicksort(lista, lambda par: par[1]) == [("b", 0), ("a", 1), ("c", 1)]


def test_quicksort_lista_grande_ya_ordenada():
    """Límite: el pivote central evita superar el límite de recursión de Python."""
    lista = list(range(5000))
    assert _quicksort(lista, lambda valor: valor) == lista


# --- Consultas compartidas ---

def test_consultar_estado_alquilada(reservas):
    """El rango cae sobre una reserva alquilada."""
    assert _consultar_estado_carpa(reservas, 1, "05/02/2027", "06/02/2027") == "alquilada"


def test_consultar_estado_reservada(reservas):
    """El rango cae sobre una reserva sin pagar."""
    assert _consultar_estado_carpa(reservas, 1, "20/01/2027", "21/01/2027") == "reservada"


def test_consultar_estado_libre_sin_superposicion(reservas):
    """La carpa tiene reservas, pero en otras fechas."""
    assert _consultar_estado_carpa(reservas, 1, "01/03/2027", "02/03/2027") == ESTADO_LIBRE


def test_consultar_estado_otra_carpa(reservas):
    """Una reserva de la carpa 1 no ocupa a la carpa 2."""
    assert _consultar_estado_carpa(reservas, 2, "05/02/2027", "06/02/2027") == ESTADO_LIBRE


def test_esta_ocupada(reservas):
    """Ocupada en el rango de una reserva y libre fuera de él."""
    assert _esta_ocupada(reservas, 1, "05/02/2027", "06/02/2027") is True
    assert _esta_ocupada(reservas, 1, "01/03/2027", "02/03/2027") is False


def test_nombre_cliente(clientes):
    """Búsqueda exitosa y búsqueda sin resultado."""
    assert _nombre_cliente(clientes, 30111222) == "Juan Pérez"
    assert _nombre_cliente(clientes, 1) == "(desconocido)"


# --- Lectura por teclado ---

def test_leer_entero_reintenta(simular_teclado):
    """Rechaza texto y valores menores al mínimo hasta recibir uno válido."""
    simular_teclado(["abc", "0", "5"])
    assert _leer_entero("", 1) == 5


def test_leer_texto_reintenta_y_limpia(simular_teclado):
    """Rechaza texto vacío y quita los espacios sobrantes."""
    simular_teclado(["   ", "  hola "])
    assert _leer_texto("") == "hola"


def test_leer_fecha_reintenta(simular_teclado):
    """Rechaza una fecha inexistente."""
    simular_teclado(["31/04/2027", "30/04/2027"])
    assert _leer_fecha("") == "30/04/2027"


def test_leer_rango_rechaza_invertido(simular_teclado):
    """Vuelve a pedir ambas fechas si desde es posterior a hasta, y devuelve una tupla."""
    simular_teclado(["10/01/2027", "01/01/2027", "01/01/2027", "10/01/2027"])
    assert _leer_rango_fechas() == ("01/01/2027", "10/01/2027")
