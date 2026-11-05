# Sombrita - Gestión de clientes, reservas y alquileres: lógica y submenú.
# Los clientes se registran al cargar una reserva, por eso están en este módulo.

from src.comunes import (
    ESTADO_ALQUILADA,
    ESTADO_RESERVADA,
    ESTADOS_RESERVA,
    _esta_ocupada,
    _fecha_de_hoy,
    _leer_entero,
    _leer_fecha,
    _leer_rango_fechas,
    _leer_texto,
    _mostrar_error,
    _mostrar_menu,
    _mostrar_resultado,
    _mostrar_tabla,
    _nombre_cliente,
    _quicksort,
    _se_superponen,
    _texto_a_fecha,
    _validar_fecha,
)
from src.persistencia import _guardar_datos

# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------


def _normalizar_nombre(nombre: str) -> str:
    """
    Contrato:
        Elimina espacios sobrantes y capitaliza cada palabra de un nombre.

    Precondiciones:
        nombre debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve el nombre normalizado, por ejemplo "  juan   PÉREZ " -> "Juan Pérez".
    """
    return " ".join(nombre.split()).title()


def _validar_telefono(telefono: str) -> bool:
    """
    Contrato:
        Verifica que un teléfono contenga solo dígitos, espacios, "+" o "-".

    Precondiciones:
        telefono debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve True si solo tiene esos caracteres y al menos 6 dígitos.
        Devuelve False en caso contrario.
    """
    cantidad_digitos = 0
    for caracter in telefono.strip():
        if caracter.isdecimal():
            cantidad_digitos += 1
        elif caracter not in " +-":
            return False
    return cantidad_digitos >= 6


def _registrar_cliente(
    clientes: dict[int, dict], dni: int, nombre: str, telefono: str
) -> bool:
    """
    Contrato:
        Da de alta un cliente con el nombre normalizado.

    Precondiciones:
        clientes debe respetar el contrato de datos.

    Postcondiciones:
        Agrega el cliente y devuelve True.
        Devuelve False, sin modificar nada, si dni <= 0, ya existe, el nombre queda vacío
        o el teléfono no es válido.
    """
    nombre_normalizado = _normalizar_nombre(nombre)
    if dni <= 0 or dni in clientes or nombre_normalizado == "":
        return False
    if not _validar_telefono(telefono):
        return False
    clientes[dni] = {"nombre": nombre_normalizado, "telefono": telefono.strip()}
    return True


def _buscar_cliente_por_nombre(clientes: dict[int, dict], texto: str) -> list[int]:
    """
    Contrato:
        Busca clientes cuyo nombre contenga un texto, sin distinguir mayúsculas.

    Precondiciones:
        clientes debe respetar el contrato de datos.

    Postcondiciones:
        Devuelve una lista con los DNI que coinciden (puede ser vacía).
    """
    texto_buscado = texto.strip().lower()
    return [
        dni
        for dni, datos in clientes.items()
        if texto_buscado in datos["nombre"].lower()
    ]


# ---------------------------------------------------------------------------
# Reservas y alquileres
# ---------------------------------------------------------------------------


def _buscar_reserva(reservas: list[dict], num_carpa: int, dni: int, desde: str) -> int:
    """
    Contrato:
        Busca una reserva por carpa, cliente y fecha de inicio.

    Precondiciones:
        desde debe ser una fecha válida.

    Postcondiciones:
        Devuelve el índice de la reserva en la lista, o -1 si no existe.
    """
    for indice, reserva in enumerate(reservas):
        if (
            reserva["carpa"] == num_carpa
            and reserva["dni"] == dni
            and reserva["desde"] == desde
        ):
            return indice
    return -1


def _registrar_reserva(
    reservas: list[dict],
    carpas: dict[int, bool],
    clientes: dict[int, dict],
    num_carpa: int,
    dni: int,
    desde: str,
    hasta: str,
    estado: str = ESTADO_RESERVADA,
) -> bool:
    """
    Contrato:
        Da de alta una reserva o alquiler de una carpa para un cliente.

    Precondiciones:
        Las estructuras deben respetar el contrato de datos.

    Postcondiciones:
        Agrega la reserva y devuelve True.
        Devuelve False, sin modificar nada, si la carpa no existe o está inactiva, el
        cliente no existe, alguna fecha no es válida, desde > hasta, el estado no está en
        ESTADOS_RESERVA o la carpa ya está ocupada en ese rango.
    """
    if not carpas.get(num_carpa, False) or dni not in clientes:
        return False
    if not (_validar_fecha(desde) and _validar_fecha(hasta)):
        return False
    if _texto_a_fecha(desde) > _texto_a_fecha(hasta):
        return False
    if estado not in ESTADOS_RESERVA or _esta_ocupada(
        reservas, num_carpa, desde, hasta
    ):
        return False

    reservas.append(
        {
            "carpa": num_carpa,
            "dni": dni,
            "desde": desde,
            "hasta": hasta,
            "estado": estado,
        }
    )
    return True


def _cancelar_reserva(
    reservas: list[dict], num_carpa: int, dni: int, desde: str
) -> bool:
    """
    Contrato:
        Da de baja una reserva.

    Precondiciones:
        desde debe ser una fecha válida.

    Postcondiciones:
        Elimina la reserva y devuelve True, o devuelve False si no existe.
    """
    indice = _buscar_reserva(reservas, num_carpa, dni, desde)
    if indice == -1:
        return False
    reservas.pop(indice)
    return True


def _cambiar_estado_reserva(
    reservas: list[dict], num_carpa: int, dni: int, desde: str, estado: str
) -> bool:
    """
    Contrato:
        Cambia el estado de una reserva a "reservada" o "alquilada".

    Precondiciones:
        desde debe ser una fecha válida.

    Postcondiciones:
        Actualiza el estado y devuelve True.
        Devuelve False, sin modificar nada, si la reserva no existe o el estado no está
        en ESTADOS_RESERVA.
    """
    indice = _buscar_reserva(reservas, num_carpa, dni, desde)
    if indice == -1 or estado not in ESTADOS_RESERVA:
        return False
    reservas[indice]["estado"] = estado
    return True


def _ordenar_reservas(reservas: list[dict], criterio: str = "fecha") -> list[dict]:
    """
    Contrato:
        Ordena las reservas por fecha de inicio o por número de carpa.

    Precondiciones:
        criterio debe ser "fecha" o "carpa".

    Postcondiciones:
        Devuelve una lista nueva ordenada con _quicksort, sin modificar la original.
    """
    if criterio == "carpa":
        return _quicksort(reservas, lambda reserva: reserva["carpa"])
    return _quicksort(reservas, lambda reserva: _texto_a_fecha(reserva["desde"]))


def _consultar_reservas_cliente(reservas: list[dict], dni: int) -> list[dict]:
    """
    Contrato:
        Obtiene las reservas de un cliente ordenadas por fecha de inicio.

    Precondiciones:
        reservas debe respetar el contrato de datos.

    Postcondiciones:
        Devuelve una lista nueva (puede ser vacía).
    """
    propias = [reserva for reserva in reservas if reserva["dni"] == dni]
    return _ordenar_reservas(propias, "fecha")


def _buscar_reservas_por_texto(
    reservas: list[dict], clientes: dict[int, dict], texto: str
) -> list[dict]:
    """
    Contrato:
        Busca reservas por DNI o por parte del nombre del cliente.

    Precondiciones:
        reservas y clientes deben respetar el contrato de datos.

    Postcondiciones:
        Si texto tiene solo dígitos, lo busca como DNI exacto.
        Si no, lo busca como parte del nombre, sin distinguir mayúsculas.
        Devuelve una lista nueva ordenada por fecha de inicio (puede ser vacía).
    """
    texto_limpio = texto.strip()
    if texto_limpio.isdecimal():
        return _consultar_reservas_cliente(reservas, int(texto_limpio))

    dnis = set(_buscar_cliente_por_nombre(clientes, texto_limpio))
    encontradas = [reserva for reserva in reservas if reserva["dni"] in dnis]
    return _ordenar_reservas(encontradas, "fecha")


def _reservas_del_dia(reservas: list[dict], fecha: str) -> list[dict]:
    """
    Contrato:
        Obtiene las reservas vigentes en una fecha, ordenadas por número de carpa.

    Precondiciones:
        fecha debe ser válida según _validar_fecha.

    Postcondiciones:
        Devuelve una lista nueva (puede ser vacía). Incluye las reservas que empiezan o
        terminan ese día.
    """
    del_dia = [
        reserva
        for reserva in reservas
        if _se_superponen(reserva["desde"], reserva["hasta"], fecha, fecha)
    ]
    return _ordenar_reservas(del_dia, "carpa")


# ---------------------------------------------------------------------------
# Entrada, salida y submenú
# ---------------------------------------------------------------------------


def _leer_estado_reserva() -> str:
    """
    Contrato:
        Solicita por teclado el estado de una reserva hasta que sea válido.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Devuelve un valor de ESTADOS_RESERVA.
    """
    _mostrar_menu(
        "Estado", [(1, "Reservada (señada o sin pagar)"), (2, "Alquilada (pagada)")]
    )
    while True:
        opcion = _leer_entero("Estado: ", 1)
        if opcion == 1:
            return ESTADO_RESERVADA
        if opcion == 2:
            return ESTADO_ALQUILADA
        _mostrar_error("Error: opción inválida.")


def _leer_fecha_del_dia() -> str:
    """
    Contrato:
        Pregunta por teclado si se consulta el día de hoy u otra fecha.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Devuelve la fecha de hoy, o la fecha ingresada, válida según _validar_fecha.
    """
    hoy = _fecha_de_hoy()
    _mostrar_menu("Día a consultar", [(1, f"Hoy ({hoy})"), (2, "Otra fecha")])
    while True:
        opcion = _leer_entero("Opción: ", 1)
        if opcion == 1:
            return hoy
        if opcion == 2:
            return _leer_fecha("Fecha (dd/mm/aaaa): ")
        _mostrar_error("Error: opción inválida.")


def _mostrar_reservas(reservas: list[dict], clientes: dict[int, dict]) -> None:
    """
    Contrato:
        Muestra reservas en una tabla, con el nombre de cada cliente.

    Precondiciones:
        reservas y clientes deben respetar el contrato de datos.

    Postcondiciones:
        Imprime carpa, DNI, nombre, desde, hasta y estado de cada reserva.
        Imprime un aviso si la lista está vacía.
    """
    filas = [
        [
            reserva["carpa"],
            reserva["dni"],
            _nombre_cliente(clientes, reserva["dni"]),
            reserva["desde"],
            reserva["hasta"],
            reserva["estado"],
        ]
        for reserva in reservas
    ]
    _mostrar_tabla(
        filas,
        ["Carpa", "DNI", "Cliente", "Desde", "Hasta", "Estado"],
        "No hay reservas para mostrar.",
    )


def _opcion_registrar_reserva(
    carpas: dict[int, bool], clientes: dict[int, dict], reservas: list[dict]
) -> bool:
    """
    Contrato:
        Pide por teclado los datos de una reserva y la registra.
        Si el DNI no existe, también pide los datos del cliente y lo registra.

    Precondiciones:
        carpas, clientes y reservas deben respetar el contrato de datos.

    Postcondiciones:
        Devuelve True si cambió algún dato, aunque sea solo el cliente nuevo.
        Devuelve False si no cambió nada. Informa el resultado por pantalla.
    """
    numero = _leer_entero("Número de carpa: ", 1)
    dni = _leer_entero("DNI del cliente: ", 1)
    cliente_nuevo = False

    if dni not in clientes:
        nombre = _leer_texto("Nombre y apellido: ")
        telefono = _leer_texto("Teléfono: ")
        cliente_nuevo = _registrar_cliente(clientes, dni, nombre, telefono)
        if not cliente_nuevo:
            _mostrar_error("Error: el teléfono no es válido.")
            return False

    desde, hasta = _leer_rango_fechas()
    estado = _leer_estado_reserva()
    exito = _registrar_reserva(
        reservas, carpas, clientes, numero, dni, desde, hasta, estado
    )
    _mostrar_resultado(
        exito,
        "Reserva registrada.",
        "Error: la carpa no existe, está inactiva o está ocupada en esas fechas.",
    )
    return exito or cliente_nuevo


def _menu_reservas(
    carpas: dict[int, bool], clientes: dict[int, dict], reservas: list[dict], ruta: str
) -> None:
    """
    Contrato:
        Ejecuta el submenú de gestión de reservas y alquileres.

    Precondiciones:
        carpas, clientes y reservas deben respetar el contrato de datos.
        ruta debe ser la ruta del archivo de datos.

    Postcondiciones:
        Modifica las estructuras según lo que elija el usuario y guarda después de cada
        cambio exitoso, hasta que el usuario vuelva.
    """
    while True:
        _mostrar_menu(
            "--- Reservas y alquileres ---",
            [
                (1, "Registrar reserva / alquiler"),
                (2, "Cancelar reserva"),
                (3, "Cambiar estado de una reserva"),
                (4, "Listar reservas por fecha"),
                (5, "Listar reservas por carpa"),
                (6, "Buscar reservas por cliente"),
                (7, "Reservas del día"),
                (0, "Volver"),
            ],
        )
        opcion = _leer_entero("Opción: ")
        hubo_cambios = False

        if opcion == 1:
            hubo_cambios = _opcion_registrar_reserva(carpas, clientes, reservas)
        elif opcion == 2:
            numero = _leer_entero("Número de carpa: ", 1)
            dni = _leer_entero("DNI del cliente: ", 1)
            desde = _leer_fecha("Fecha desde de la reserva (dd/mm/aaaa): ")
            hubo_cambios = _cancelar_reserva(reservas, numero, dni, desde)
            _mostrar_resultado(
                hubo_cambios, "Reserva cancelada.", "Error: la reserva no existe."
            )
        elif opcion == 3:
            numero = _leer_entero("Número de carpa: ", 1)
            dni = _leer_entero("DNI del cliente: ", 1)
            desde = _leer_fecha("Fecha desde de la reserva (dd/mm/aaaa): ")
            estado = _leer_estado_reserva()
            hubo_cambios = _cambiar_estado_reserva(reservas, numero, dni, desde, estado)
            _mostrar_resultado(
                hubo_cambios, "Estado actualizado.", "Error: la reserva no existe."
            )
        elif opcion == 4:
            _mostrar_reservas(_ordenar_reservas(reservas, "fecha"), clientes)
        elif opcion == 5:
            _mostrar_reservas(_ordenar_reservas(reservas, "carpa"), clientes)
        elif opcion == 6:
            texto = _leer_texto("DNI o parte del nombre: ")
            _mostrar_reservas(
                _buscar_reservas_por_texto(reservas, clientes, texto), clientes
            )
        elif opcion == 7:
            fecha = _leer_fecha_del_dia()
            _mostrar_reservas(_reservas_del_dia(reservas, fecha), clientes)
        elif opcion == 0:
            return
        else:
            _mostrar_error("Opción inválida.")

        if hubo_cambios:
            _guardar_datos(ruta, carpas, clientes, reservas)
