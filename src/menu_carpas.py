# Sombrita - Gestión de carpas: lógica y submenú.

from src.comunes import (
    _consultar_estado_carpa,
    _leer_entero,
    _leer_rango_fechas,
    _mostrar_error,
    _mostrar_menu,
    _mostrar_resultado,
    _mostrar_tabla,
    _quicksort,
)
from src.persistencia import _guardar_datos


def _registrar_carpa(carpas: dict[int, bool], num_carpa: int) -> bool:
    """
    Contrato:
        Da de alta una carpa nueva, activa por defecto.

    Precondiciones:
        carpas debe respetar el contrato de datos.

    Postcondiciones:
        Agrega la carpa y devuelve True.
        Devuelve False, sin modificar nada, si num_carpa <= 0 o ya existe.
    """
    if num_carpa <= 0 or num_carpa in carpas:
        return False
    carpas[num_carpa] = True
    return True


def _modificar_carpa(
    carpas: dict[int, bool], reservas: list[dict], num_actual: int, num_nuevo: int
) -> bool:
    """
    Contrato:
        Cambia el número de una carpa y actualiza sus reservas.

    Precondiciones:
        carpas y reservas deben respetar el contrato de datos.

    Postcondiciones:
        Cambia el número, conserva el estado activa/inactiva y actualiza "carpa" en todas
        sus reservas; devuelve True.
        Devuelve False, sin modificar nada, si num_actual no existe, num_nuevo <= 0 o
        num_nuevo ya está en uso.
    """
    if num_actual not in carpas or num_nuevo <= 0 or num_nuevo in carpas:
        return False

    carpas[num_nuevo] = carpas.pop(num_actual)
    for reserva in reservas:
        if reserva["carpa"] == num_actual:
            reserva["carpa"] = num_nuevo
    return True


def _cambiar_estado_carpa(
    carpas: dict[int, bool], reservas: list[dict], num_carpa: int, activa: bool
) -> bool:
    """
    Contrato:
        Activa o inactiva una carpa (borrado lógico).

    Precondiciones:
        carpas y reservas deben respetar el contrato de datos.

    Postcondiciones:
        Actualiza el estado y devuelve True.
        Devuelve False, sin modificar nada, si la carpa no existe o si se intenta
        inactivar una carpa con reservas registradas.
    """
    if num_carpa not in carpas:
        return False

    if not activa:
        for reserva in reservas:
            if reserva["carpa"] == num_carpa:
                return False

    carpas[num_carpa] = activa
    return True


def _listar_carpas(
    carpas: dict[int, bool], solo_activas: bool = False
) -> list[tuple[int, bool]]:
    """
    Contrato:
        Obtiene las carpas ordenadas por número.

    Precondiciones:
        Carpas debe respetar el contrato de datos.

    Postcondiciones:
        Devuelve una lista nueva de tuplas (número, activa) ordenada con
        _quicksort.
        Si solo_activas es True, excluye las inactivas. No modifica carpas.
    """
    filtradas = [
        (numero, activa)
        for numero, activa in carpas.items()
        if activa or not solo_activas
    ]
    return _quicksort(filtradas, lambda carpa: carpa[0])


def _mostrar_carpas(carpas_listadas: list[tuple[int, bool]]) -> None:
    """
    Contrato:
        Muestra carpas en una tabla.

    Precondiciones:
        carpas_listadas debe tener el formato que devuelve _listar_carpas.

    Postcondiciones:
        Imprime número y estado (activa / inactiva) de cada carpa.
        Imprime un aviso si la lista está vacía.
    """
    filas = [
        [numero, "activa" if activa else "inactiva"]
        for numero, activa in carpas_listadas
    ]
    _mostrar_tabla(filas, ["Carpa", "Estado"], "No hay carpas para mostrar.")


def _menu_carpas(
    carpas: dict[int, bool], clientes: dict[int, dict], reservas: list[dict], ruta: str
) -> None:
    """
    Contrato:
        Ejecuta el submenú de gestión de carpas.

    Precondiciones:
        carpas, clientes y reservas deben respetar el contrato de datos.
        ruta debe ser la ruta del archivo de datos.

    Postcondiciones:
        Modifica las estructuras según lo que elija el usuario y guarda después de cada
        cambio exitoso, hasta que el usuario vuelva.
    """
    while True:
        _mostrar_menu(
            "--- Carpas ---",
            [
                (1, "Registrar carpa"),
                (2, "Listar carpas"),
                (3, "Modificar número de carpa"),
                (4, "Activar / Inactivar carpa"),
                (5, "Consultar estado de una carpa por fechas"),
                (0, "Volver"),
            ],
        )
        opcion = _leer_entero("Opción: ")
        exito = False

        if opcion == 1:
            numero = _leer_entero("Número de carpa: ", 1)
            exito = _registrar_carpa(carpas, numero)
            _mostrar_resultado(exito, "Carpa registrada.", "Error: la carpa ya existe.")
        elif opcion == 2:
            _mostrar_carpas(_listar_carpas(carpas))
        elif opcion == 3:
            actual = _leer_entero("Número actual: ", 1)
            nuevo = _leer_entero("Número nuevo: ", 1)
            exito = _modificar_carpa(carpas, reservas, actual, nuevo)
            _mostrar_resultado(
                exito,
                "Carpa modificada.",
                "Error: la carpa no existe o el nuevo número ya está en uso.",
            )
        elif opcion == 4:
            _mostrar_menu(
                "Activar / Inactivar carpa", [(1, "Activar"), (2, "Inactivar")]
            )
            accion = _leer_entero("Acción: ", 1)
            if accion == 1:
                numero = _leer_entero("Número de carpa: ", 1)
                exito = _cambiar_estado_carpa(carpas, reservas, numero, True)
                _mostrar_resultado(
                    exito, "Carpa activada.", "Error: la carpa no existe."
                )
            elif accion == 2:
                numero = _leer_entero("Número de carpa: ", 1)
                exito = _cambiar_estado_carpa(carpas, reservas, numero, False)
                _mostrar_resultado(
                    exito,
                    "Carpa inactivada.",
                    "Error: la carpa no existe o tiene reservas registradas.",
                )
            else:
                _mostrar_error("Opción inválida.")
        elif opcion == 5:
            numero = _leer_entero("Número de carpa: ", 1)
            if numero not in carpas:
                _mostrar_error("Error: la carpa no existe.")
            else:
                desde, hasta = _leer_rango_fechas()
                estado = _consultar_estado_carpa(reservas, numero, desde, hasta)
                print(f"La carpa {numero} está {estado} entre {desde} y {hasta}.")
        elif opcion == 0:
            return
        else:
            _mostrar_error("Opción inválida.")

        if exito:
            _guardar_datos(ruta, carpas, clientes, reservas)
