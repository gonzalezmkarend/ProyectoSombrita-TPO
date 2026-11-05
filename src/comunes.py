# Sombrita - Funciones y constantes que usan todos los módulos.
# Este módulo no importa a ningún otro módulo del proyecto.

import os
from datetime import datetime
from typing import Any, Callable

from colorama import Fore, Style
from tabulate import tabulate

ESTADO_LIBRE: str = "libre"
ESTADO_RESERVADA: str = "reservada"
ESTADO_ALQUILADA: str = "alquilada"
ESTADOS_RESERVA: tuple[str, str] = (ESTADO_RESERVADA, ESTADO_ALQUILADA)

FORMATO_FECHA: str = "%d/%m/%Y"
LARGO_FECHA: int = 10
FORMATO_TABLA: str = "rounded_outline"

RAIZ_PROYECTO: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO_DATOS: str = os.path.join(RAIZ_PROYECTO, "datos", "sombrita.json")


# ---------------------------------------------------------------------------
# Fechas
# ---------------------------------------------------------------------------


def _validar_fecha(fecha: str) -> bool:
    """
    Contrato:
        Verifica que una cadena tenga formato "dd/mm/aaaa" y represente
        una fecha existente.

    Precondiciones:
        fecha debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve True si la fecha es válida, teniendo en cuenta los años bisiestos.
        Devuelve False en caso contrario. No lanza excepciones.
    """
    fecha_limpia = fecha.strip()
    if len(fecha_limpia) != LARGO_FECHA:
        return False
    try:
        datetime.strptime(fecha_limpia, FORMATO_FECHA)
    except ValueError:
        return False
    return True


def _texto_a_fecha(fecha: str) -> datetime:
    """
    Contrato:
        Convierte una fecha "dd/mm/aaaa" en un objeto datetime para poder compararla.

    Precondiciones:
        fecha debe ser válida según _validar_fecha.

    Postcondiciones:
        Devuelve el datetime correspondiente; una fecha más tardía genera un valor mayor.
    """
    return datetime.strptime(fecha.strip(), FORMATO_FECHA)


def _fecha_de_hoy() -> str:
    """
    Contrato:
        Obtiene la fecha actual del sistema.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Devuelve la fecha de hoy como texto "dd/mm/aaaa", válida según 
        _validar_fecha.
    """
    return datetime.now().strftime(FORMATO_FECHA)


def _se_superponen(desde1: str, hasta1: str, desde2: str, hasta2: str) -> bool:
    """
    Contrato:
        Indica si dos rangos de fechas comparten al menos un día.

    Precondiciones:
        Las fechas deben ser válidas y cada rango debe cumplir desde <= hasta.

    Postcondiciones:
        Devuelve True si los rangos comparten algún día, incluidos los extremos.
        Devuelve False en caso contrario.
    """
    return _texto_a_fecha(desde1) <= _texto_a_fecha(hasta2) and _texto_a_fecha(
        desde2) <= _texto_a_fecha(hasta1)


# ---------------------------------------------------------------------------
# Ordenamiento
# ---------------------------------------------------------------------------


def _quicksort(lista: list[Any], clave: Callable[[Any], Any]) -> list:
    """
    Contrato:
        Ordena una lista de menor a mayor con quicksort recursivo, según
        una función clave.

    Precondiciones:
        Clave debe recibir un elemento de la lista y devolver un valor
        comparable.

    Postcondiciones:
        Devuelve una lista nueva ordenada, sin modificar la original.
        Los elementos con la misma clave conservan su orden relativo.
    """
    if len(lista) <= 1:
        return list(lista)

    clave_pivote = clave(lista[len(lista) // 2])
    menores = [elemento for elemento in lista if clave(elemento) < clave_pivote]
    iguales = [elemento for elemento in lista if clave(elemento) == clave_pivote]
    mayores = [elemento for elemento in lista if clave(elemento) > clave_pivote]
    return _quicksort(menores, clave) + iguales + _quicksort(mayores, clave)


# ---------------------------------------------------------------------------
# Consultas que comparten varios menús
# ---------------------------------------------------------------------------


def _consultar_estado_carpa(
    reservas: list[dict], num_carpa: int, desde: str, hasta: str
) -> str:
    """
    Contrato:
        Obtiene el estado de una carpa en un rango de fechas.

    Precondiciones:
        Las fechas deben ser válidas y cumplir desde <= hasta.

    Postcondiciones:
        Devuelve el estado de la primera reserva superpuesta ("reservada" o "alquilada").
        Devuelve ESTADO_LIBRE si no hay ninguna.
    """
    for reserva in reservas:
        if reserva["carpa"] == num_carpa and _se_superponen(
            reserva["desde"], reserva["hasta"], desde, hasta
        ):
            return reserva["estado"]
    return ESTADO_LIBRE


def _esta_ocupada(reservas: list[dict], num_carpa: int, desde: str, hasta: str) -> bool:
    """
    Contrato:
        Indica si una carpa tiene alguna reserva superpuesta a un rango de fechas.

    Precondiciones:
        Las fechas deben ser válidas y cumplir desde <= hasta.

    Postcondiciones:
        Devuelve True si está ocupada algún día del rango, False si está libre.
    """
    return _consultar_estado_carpa(reservas, num_carpa, desde, hasta) != ESTADO_LIBRE


def _nombre_cliente(clientes: dict[int, dict], dni: int) -> str:
    """
    Contrato:
        Obtiene el nombre de un cliente a partir de su DNI.

    Precondiciones:
        clientes debe respetar el contrato de datos.

    Postcondiciones:
        Devuelve el nombre, o "(desconocido)" si el DNI no existe.
    """
    if dni in clientes:
        return clientes[dni]["nombre"]
    return "(desconocido)"


# ---------------------------------------------------------------------------
# Salida por pantalla
# ---------------------------------------------------------------------------


def _mostrar_error(mensaje: str) -> None:
    """
    Contrato:
        Muestra un mensaje de error en color rojo.

    Precondiciones:
        Mensaje debe ser una cadena de caracteres.

    Postcondiciones:
        Imprime el mensaje por pantalla.
    """
    print(f"{Fore.RED}{mensaje}{Style.RESET_ALL}")


def _mostrar_exito(mensaje: str) -> None:
    """
    Contrato:
        Muestra un mensaje de éxito en color verde.

    Precondiciones:
        mensaje debe ser una cadena de caracteres.

    Postcondiciones:
        Imprime el mensaje por pantalla.
    """
    print(f"{Fore.GREEN}{mensaje}{Style.RESET_ALL}")


def _mostrar_resultado(exito: bool, mensaje_ok: str, mensaje_error: str) -> None:
    """
    Contrato:
        Muestra un mensaje según el resultado de una operación.

    Precondiciones:
        mensaje_ok y mensaje_error deben ser cadenas de caracteres.

    Postcondiciones:
        Imprime mensaje_ok en verde si exito es True, o mensaje_error en rojo si es False.
    """
    if exito:
        _mostrar_exito(mensaje_ok)
    else:
        _mostrar_error(mensaje_error)


def _mostrar_menu(titulo: str, opciones: list[tuple[int, str]]) -> None:
    """
    Contrato:
        Muestra un menú como tabla, con el título resaltado en color.

    Precondiciones:
        Título debe ser una cadena de caracteres.
        Opciones debe ser una lista de tuplas (número, descripción).

    Postcondiciones:
        Imprime el título y la tabla de opciones por pantalla.
    """
    print(f"\n{Style.BRIGHT}{Fore.CYAN}{titulo}{Style.RESET_ALL}")
    print(tabulate(opciones, headers=["Opción", "Descripción"], tablefmt=FORMATO_TABLA))


def _mostrar_tabla(filas: list[list], encabezados: list[str], aviso_vacio: str) -> None:
    """
    Contrato:
        Muestra datos en una tabla, o un aviso si no hay datos.

    Precondiciones:
        Cada fila debe tener un valor por cada encabezado.

    Postcondiciones:
        Imprime la tabla por pantalla, o aviso_vacio en amarillo si
        filas está vacía.
    """
    if len(filas) == 0:
        print(f"{Fore.YELLOW}{aviso_vacio}{Style.RESET_ALL}")
        return
    print(tabulate(filas, headers=encabezados, tablefmt=FORMATO_TABLA))


# ---------------------------------------------------------------------------
# Entrada por teclado
# ---------------------------------------------------------------------------


def _leer_entero(mensaje: str, minimo: int = 0) -> int:
    """
    Contrato:
        Solicita un número entero por teclado hasta que sea válido.

    Precondiciones:
        mensaje debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve un entero mayor o igual a minimo.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            _mostrar_error(f"Error: debe ingresar un número mayor o igual a {minimo}.")
        except ValueError:
            _mostrar_error("Error: debe ingresar un número entero.")


def _leer_texto(mensaje: str) -> str:
    """
    Contrato:
        Solicita un texto no vacío por teclado.

    Precondiciones:
        mensaje debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve el texto ingresado, sin espacios al inicio ni al final.
    """
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        _mostrar_error("Error: el texto no puede estar vacío.")


def _leer_fecha(mensaje: str) -> str:
    """
    Contrato:
        Solicita una fecha "dd/mm/aaaa" por teclado hasta que sea válida.

    Precondiciones:
        mensaje debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve una fecha válida según _validar_fecha, sin espacios sobrantes.
    """
    while True:
        fecha = input(mensaje).strip()
        if _validar_fecha(fecha):
            return fecha
        _mostrar_error(
            "Error: la fecha debe tener formato dd/mm/aaaa y ser una fecha existente."
        )


def _leer_rango_fechas() -> tuple[str, str]:
    """
    Contrato:
        Solicita dos fechas, desde y hasta, hasta que formen un rango válido.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Devuelve la tupla (desde, hasta) con fechas válidas y desde <= hasta.
    """
    while True:
        desde = _leer_fecha("Fecha desde (dd/mm/aaaa): ")
        hasta = _leer_fecha("Fecha hasta (dd/mm/aaaa): ")
        if _texto_a_fecha(desde) <= _texto_a_fecha(hasta):
            return (desde, hasta)
        _mostrar_error(
            "Error: la fecha 'desde' no puede ser posterior a la fecha 'hasta'."
        )
