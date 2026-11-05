# Sombrita - Sistema de gestión de alquiler de carpas de un balneario.
# Punto de entrada: carga los datos e integra los tres menús.

from colorama import init

from src.comunes import (
    ARCHIVO_DATOS,
    _leer_entero,
    _mostrar_error,
    _mostrar_exito,
    _mostrar_menu,
    _limpiar_consola,
)
from src.menu_carpas import _menu_carpas
from src.menu_estadisticas import _menu_estadisticas
from src.menu_reservas import _menu_reservas
from src.persistencia import _cargar_datos, _guardar_datos


def main() -> None:
    """
    Contrato:
        Ejecuta el programa principal: carga los datos y muestra el menú.

    Precondiciones:
        El archivo debe ejecutarse como programa principal.

    Postcondiciones:
        Permite navegar los submenús hasta que el usuario elija salir o 
        interrumpa con Ctrl+C. En ambos casos guarda los datos antes 
        de terminar.
    """
    init()
    carpas, clientes, reservas = _cargar_datos(ARCHIVO_DATOS)

    try:
        while True:
            _limpiar_consola()
            _mostrar_menu(
                "===== Sombrita: gestión de carpas del balneario =====",
                [
                    (1, "Carpas"),
                    (2, "Reservas y alquileres"),
                    (3, "Estadísticas"),
                    (0, "Salir"),
                ],
            )
            opcion = _leer_entero("Opción: ")

            if opcion == 1:
                _menu_carpas(carpas, clientes, reservas, ARCHIVO_DATOS)
            elif opcion == 2:
                _menu_reservas(carpas, clientes, reservas, ARCHIVO_DATOS)
            elif opcion == 3:
                _menu_estadisticas(carpas, clientes, reservas)
            elif opcion == 0:
                break
            else:
                _mostrar_error("Opción inválida.")
    except (KeyboardInterrupt, EOFError):
        print()

    _guardar_datos(ARCHIVO_DATOS, carpas, clientes, reservas)
    _mostrar_exito("Hasta luego.")


if __name__ == "__main__":
    main()
