# TPO - Etapa 1
# Sistema de gestión de alquiler de carpas de un balneario.
# Esqueleto del menú: cada opción muestra qué va a hacer, sin implementarlo todavía.


def _leer_entero(mensaje: str, minimo: int = 0) -> int:
    """
    Contrato:
        Solicita un número entero por teclado hasta que sea válido.

    Precondiciones:
        El mensaje debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve un entero mayor o igual a minimo.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            print(f"Error: debe ingresar un número mayor o igual a {minimo}.")
        except ValueError:
            print("Error: debe ingresar un número entero.")


def _pendiente(descripcion: str) -> None:
    """
    Contrato:
        Muestra la descripción de una funcionalidad todavía no implementada.

    Precondiciones:
        La descripción debe ser una cadena de caracteres.

    Postcondiciones:
        Imprime la descripción por pantalla.
    """
    print(f"[Pendiente] {descripcion}")


# ---------------------------------------------------------------------------
# Submenús
# ---------------------------------------------------------------------------

def _menu_carpas() -> None:
    """
    Contrato:
        Ejecuta el submenú de gestión de carpas.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Muestra por pantalla la descripción de la opción elegida hasta que el usuario vuelva.
    """
    while True:
        print("\n--- Carpas ---")
        print("1. Registrar carpa")
        print("2. Listar carpas")
        print("3. Modificar número de carpa")
        print("4. Activar / Inactivar carpa")
        print("5. Consultar estado de una carpa por fechas")
        print("0. Volver")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            _pendiente("Registrar carpa: pide un número, valida que sea mayor a 0 y que no "
                       "exista, y agrega la carpa como activa.")
        elif opcion == 2:
            _pendiente("Listar carpas: muestra todas las carpas ordenadas por número con su "
                       "estado (activa / inactiva).")
        elif opcion == 3:
            _pendiente("Modificar carpa: pide el número actual y el nuevo, valida que el nuevo "
                       "no esté en uso y actualiza la carpa y sus reservas.")
        elif opcion == 4:
            print("  1. Activar")
            print("  2. Inactivar")
            accion = _leer_entero("Acción: ", 1)
            if accion == 1:
                _pendiente("Activar carpa: pide el número y vuelve a marcar como activa una "
                           "carpa inactiva.")
            elif accion == 2:
                _pendiente("Inactivar carpa: pide el número y marca la carpa como inactiva "
                           "(borrado lógico). No se permite si tiene reservas registradas.")
            else:
                print("Opción inválida.")
        elif opcion == 5:
            _pendiente("Consultar estado: pide número de carpa y rango de fechas, y responde si "
                       "está libre, reservada o alquilada en ese rango.")
        elif opcion == 0:
            return
        else:
            print("Opción inválida.")


def _menu_reservas() -> None:
    """
    Contrato:
        Ejecuta el submenú de gestión de reservas y alquileres.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Muestra por pantalla la descripción de la opción elegida hasta que el usuario vuelva.
    """
    while True:
        print("\n--- Reservas y alquileres ---")
        print("1. Registrar reserva / alquiler")
        print("2. Cancelar reserva")
        print("3. Cambiar estado de una reserva")
        print("4. Listar reservas por fecha")
        print("5. Listar reservas por carpa")
        print("6. Buscar reservas por cliente")
        print("7. Reservas del día")
        print("0. Volver")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            _pendiente("Registrar reserva: pide carpa, datos del cliente (DNI, nombre y "
                       "teléfono), rango de fechas y estado (reservada = señada o sin pagar / "
                       "alquilada = pagada). Valida que la carpa exista y esté activa, que los "
                       "datos del cliente sean válidos, que las fechas sean válidas y que la "
                       "carpa no esté ocupada en ese rango.")
        elif opcion == 2:
            _pendiente("Cancelar reserva: pide carpa, DNI y fecha de inicio, y elimina la "
                       "reserva si existe.")
        elif opcion == 3:
            _pendiente("Cambiar estado: pide carpa, DNI y fecha de inicio, y pasa la reserva a "
                       "alquilada (se pagó) o de vuelta a reservada.")
        elif opcion == 4:
            _pendiente("Listar reservas por fecha: muestra todas las reservas ordenadas por "
                       "fecha de inicio, con los datos del cliente.")
        elif opcion == 5:
            _pendiente("Listar reservas por carpa: muestra todas las reservas ordenadas por "
                       "número de carpa, con los datos del cliente.")
        elif opcion == 6:
            _pendiente("Buscar reservas por cliente: pide un DNI o parte del nombre y muestra "
                       "las reservas de ese cliente, sin distinguir mayúsculas.")
        elif opcion == 7:
            _pendiente("Reservas del día: pide una fecha y muestra las reservas vigentes ese "
                       "día ordenadas por carpa (notificaciones del día).")
        elif opcion == 0:
            return
        else:
            print("Opción inválida.")


def _menu_estadisticas() -> None:
    """
    Contrato:
        Ejecuta el submenú de estadísticas.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Muestra por pantalla la descripción de la opción elegida hasta que el usuario vuelva.
    """
    while True:
        print("\n--- Estadísticas ---")
        print("1. Porcentaje de ocupación en un rango de fechas")
        print("2. Carpas libres en un rango de fechas")
        print("3. Cliente con más reservas")
        print("0. Volver")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            _pendiente("Ocupación: pide un rango de fechas y calcula el porcentaje de carpas "
                       "activas que tienen alguna reserva en ese rango.")
        elif opcion == 2:
            _pendiente("Carpas libres: pide un rango de fechas y muestra las carpas activas sin "
                       "ninguna reserva en ese rango, ordenadas por número.")
        elif opcion == 3:
            _pendiente("Cliente con más reservas: cuenta las reservas por DNI y muestra el "
                       "cliente que tiene más.")
        elif opcion == 0:
            return
        else:
            print("Opción inválida.")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Contrato:
        Ejecuta el programa principal y muestra el menú.

    Precondiciones:
        El archivo debe ejecutarse como programa principal.

    Postcondiciones:
        Permite navegar los submenús hasta que el usuario elija salir.
    """
    while True:
        print("\n===== Gestión de carpas del balneario =====")
        print("1. Carpas")
        print("2. Reservas y alquileres")
        print("3. Estadísticas")
        print("0. Salir")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            _menu_carpas()
        elif opcion == 2:
            _menu_reservas()
        elif opcion == 3:
            _menu_estadisticas()
        elif opcion == 0:
            print("Hasta luego.")
            return
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()