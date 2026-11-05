# Sombrita - Estadísticas: lógica y submenú. Este módulo solo lee los datos, no los modifica.

from src.comunes import (
    _leer_entero,
    _leer_rango_fechas,
    _mostrar_error,
    _mostrar_menu,
    _mostrar_tabla,
    _nombre_cliente,
    _quicksort,
    _se_superponen,
)


def _carpas_ocupadas(reservas: list[dict], desde: str, hasta: str) -> set[int]:
    """
    Contrato:
        Obtiene los números de carpa con alguna reserva superpuesta a un rango de fechas.

    Precondiciones:
        Las fechas deben ser válidas y cumplir desde <= hasta.

    Postcondiciones:
        Devuelve un conjunto de números de carpa (puede ser vacío).
    """
    return {reserva["carpa"] for reserva in reservas
            if _se_superponen(reserva["desde"], reserva["hasta"], desde, hasta)}


def _carpas_libres(carpas: dict[int, bool], reservas: list[dict], desde: str,
                   hasta: str) -> list[int]:
    """
    Contrato:
        Obtiene las carpas activas sin ninguna reserva en un rango de fechas.

    Precondiciones:
        Las fechas deben ser válidas y cumplir desde <= hasta.

    Postcondiciones:
        Devuelve una lista nueva de números de carpa ordenada de menor a mayor
        (puede ser vacía). Excluye las carpas inactivas.
    """
    ocupadas = _carpas_ocupadas(reservas, desde, hasta)
    libres = [numero for numero, activa in carpas.items() if activa and numero not in ocupadas]
    return _quicksort(libres, lambda numero: numero)


def _calcular_ocupacion(carpas: dict[int, bool], reservas: list[dict], desde: str,
                        hasta: str) -> float:
    """
    Contrato:
        Calcula el porcentaje de carpas activas con alguna reserva en un rango de fechas.

    Precondiciones:
        Las fechas deben ser válidas y cumplir desde <= hasta.

    Postcondiciones:
        Devuelve un valor entre 0.0 y 100.0, sin redondear.
        Devuelve 0.0 si no hay carpas activas.
    """
    activas = {numero for numero, activa in carpas.items() if activa}
    if len(activas) == 0:
        return 0.0
    ocupadas = activas & _carpas_ocupadas(reservas, desde, hasta)
    return len(ocupadas) * 100 / len(activas)


def _dnis_con_reservas(reservas: list[dict]) -> set[int]:
    """
    Contrato:
        Obtiene los DNI distintos que aparecen en las reservas.

    Precondiciones:
        reservas debe respetar el contrato de datos.

    Postcondiciones:
        Devuelve un conjunto de DNI (vacío si no hay reservas).
    """
    return {reserva["dni"] for reserva in reservas}


def _contar_reservas_cliente(reservas: list[dict], dni: int) -> int:
    """
    Contrato:
        Cuenta las reservas de un cliente.

    Precondiciones:
        reservas debe respetar el contrato de datos.

    Postcondiciones:
        Devuelve la cantidad de reservas con ese DNI (0 si no tiene).
    """
    cantidad = 0
    for reserva in reservas:
        if reserva["dni"] == dni:
            cantidad += 1
    return cantidad


def _cliente_con_mas_reservas(reservas: list[dict]) -> int | None:
    """
    Contrato:
        Encuentra el cliente con mayor cantidad de reservas.

    Precondiciones:
        reservas debe respetar el contrato de datos.

    Postcondiciones:
        Devuelve el DNI del cliente con más reservas; si hay empate, el DNI menor.
        Devuelve None si no hay reservas.
    """
    mejor_dni = None
    mejor_cantidad = 0
    for dni in _quicksort(list(_dnis_con_reservas(reservas)), lambda valor: valor):
        cantidad = _contar_reservas_cliente(reservas, dni)
        if cantidad > mejor_cantidad:
            mejor_dni = dni
            mejor_cantidad = cantidad
    return mejor_dni


def _menu_estadisticas(carpas: dict[int, bool], clientes: dict[int, dict],
                       reservas: list[dict]) -> None:
    """
    Contrato:
        Ejecuta el submenú de estadísticas.

    Precondiciones:
        carpas, clientes y reservas deben respetar el contrato de datos.

    Postcondiciones:
        Muestra por pantalla la información elegida hasta que el usuario vuelva.
        No modifica ninguna estructura.
    """
    while True:
        _mostrar_menu("--- Estadísticas ---", [
            (1, "Porcentaje de ocupación en un rango de fechas"),
            (2, "Carpas libres en un rango de fechas"),
            (3, "Cliente con más reservas"),
            (0, "Volver"),
        ])
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            desde, hasta = _leer_rango_fechas()
            ocupacion = _calcular_ocupacion(carpas, reservas, desde, hasta)
            print(f"Ocupación entre {desde} y {hasta}: {ocupacion:.1f}%")
        elif opcion == 2:
            desde, hasta = _leer_rango_fechas()
            filas = [[numero] for numero in _carpas_libres(carpas, reservas, desde, hasta)]
            _mostrar_tabla(filas, ["Carpa libre"], "No hay carpas libres en ese rango.")
        elif opcion == 3:
            dni = _cliente_con_mas_reservas(reservas)
            if dni is None:
                print("No hay reservas registradas.")
            else:
                cantidad = _contar_reservas_cliente(reservas, dni)
                print(f"{_nombre_cliente(clientes, dni)} (DNI {dni}) con {cantidad} reserva(s).")
        elif opcion == 0:
            return
        else:
            _mostrar_error("Opción inválida.")
