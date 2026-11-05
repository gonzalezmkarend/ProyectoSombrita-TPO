# TPO - Etapa 1
# Sistema de gestión de alquiler de carpas de un balneario.
#
# Estructuras de datos (listas):
#   carpa   = [num_carpa, activa]
#   cliente = [dni, nombre, telefono]
#   reserva = [num_carpa, dni, fecha_desde, fecha_hasta, estado]
#
# El estado de una carpa ("libre", "reservada" o "alquilada") no se guarda:
# se calcula a partir de las reservas para una fecha o rango de fechas.

# Índices de cada registro
CARPA_NUM = 0
CARPA_ACTIVA = 1

CLIENTE_DNI = 0
CLIENTE_NOMBRE = 1
CLIENTE_TELEFONO = 2

RESERVA_CARPA = 0
RESERVA_DNI = 1
RESERVA_DESDE = 2
RESERVA_HASTA = 3
RESERVA_ESTADO = 4

ESTADO_LIBRE = "libre"
ESTADO_RESERVADA = "reservada"
ESTADO_ALQUILADA = "alquilada"


# ---------------------------------------------------------------------------
# Fechas
# ---------------------------------------------------------------------------

def _es_bisiesto(anio: int) -> bool:
    """
    Contrato:
        Indica si un año es bisiesto.

    Precondiciones:
        El año debe ser un entero positivo.

    Postcondiciones:
        Devuelve True si el año es bisiesto, False en caso contrario.
    """
    return (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0


def _validar_fecha(fecha: str) -> bool:
    """
    Contrato:
        Verifica que una cadena tenga formato "dd/mm/aaaa" y represente una fecha existente.

    Precondiciones:
        La fecha debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve True si la fecha es válida, False en caso contrario.
    """
    partes = fecha.strip().split("/")
    if len(partes) != 3:
        return False
    dia, mes, anio = partes
    if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
        return False
    if len(dia) != 2 or len(mes) != 2 or len(anio) != 4:
        return False

    dia, mes, anio = int(dia), int(mes), int(anio)
    if mes < 1 or mes > 12:
        return False

    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if mes == 2 and _es_bisiesto(anio):
        dias_por_mes[1] = 29

    return 1 <= dia <= dias_por_mes[mes - 1]


def _fecha_a_clave(fecha: str) -> int:
    """
    Contrato:
        Convierte una fecha "dd/mm/aaaa" en un entero aaaammdd que permite compararla.

    Precondiciones:
        La fecha debe ser válida según _validar_fecha.

    Postcondiciones:
        Devuelve un entero mayor cuanto más tardía es la fecha.
    """
    dia, mes, anio = fecha.strip().split("/")
    return int(anio) * 10000 + int(mes) * 100 + int(dia)


def _comparar_fechas(fecha1: str, fecha2: str) -> int:
    """
    Contrato:
        Compara dos fechas.

    Precondiciones:
        Ambas fechas deben ser válidas.

    Postcondiciones:
        Devuelve -1 si fecha1 es anterior, 0 si son iguales y 1 si es posterior.
    """
    clave1 = _fecha_a_clave(fecha1)
    clave2 = _fecha_a_clave(fecha2)
    if clave1 < clave2:
        return -1
    if clave1 > clave2:
        return 1
    return 0


def _se_superponen(desde1: str, hasta1: str, desde2: str, hasta2: str) -> bool:
    """
    Contrato:
        Indica si dos rangos de fechas comparten al menos un día.

    Precondiciones:
        Las fechas deben ser válidas y cada rango debe cumplir desde <= hasta.

    Postcondiciones:
        Devuelve True si los rangos se superponen, False en caso contrario.
    """
    return (_comparar_fechas(desde1, hasta2) <= 0
            and _comparar_fechas(desde2, hasta1) <= 0)


# ---------------------------------------------------------------------------
# Cadenas, validaciones y ordenamiento
# ---------------------------------------------------------------------------

def _normalizar_nombre(nombre: str) -> str:
    """
    Contrato:
        Elimina espacios sobrantes y capitaliza cada palabra del nombre.

    Precondiciones:
        El nombre debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve el nombre normalizado, por ejemplo "  juan   PÉREZ " -> "Juan Pérez".
    """
    palabras = nombre.split()
    return " ".join(palabras).title()


def _validar_telefono(telefono: str) -> bool:
    """
    Contrato:
        Verifica que un teléfono contenga solo dígitos, espacios, "+" o "-" y al menos 6 dígitos.

    Precondiciones:
        El teléfono debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve True si el teléfono es válido, False en caso contrario.
    """
    telefono = telefono.strip()
    cantidad_digitos = 0
    for caracter in telefono:
        if caracter.isdigit():
            cantidad_digitos += 1
        elif caracter not in " +-":
            return False
    return cantidad_digitos >= 6


def _ordenar(lista: list, clave) -> list:
    """
    Contrato:
        Ordena una lista de menor a mayor por inserción, según una función clave.

    Precondiciones:
        clave debe ser una función que reciba un elemento y devuelva un valor comparable.

    Postcondiciones:
        Devuelve una lista nueva ordenada; no modifica la original.
    """
    ordenada = list(lista)
    for i in range(1, len(ordenada)):
        actual = ordenada[i]
        j = i - 1
        while j >= 0 and clave(ordenada[j]) > clave(actual):
            ordenada[j + 1] = ordenada[j]
            j -= 1
        ordenada[j + 1] = actual
    return ordenada


# ---------------------------------------------------------------------------
# Carpas
# ---------------------------------------------------------------------------

def _buscar_carpa(carpas: list, num_carpa: int) -> int:
    """
    Contrato:
        Busca una carpa por número.

    Precondiciones:
        carpas debe ser una lista de carpas.

    Postcondiciones:
        Devuelve el índice de la carpa en la lista o -1 si no existe.
    """
    for indice, carpa in enumerate(carpas):
        if carpa[CARPA_NUM] == num_carpa:
            return indice
    return -1


def _registrar_carpa(carpas: list, num_carpa: int) -> bool:
    """
    Contrato:
        Da de alta una carpa nueva, activa por defecto.

    Precondiciones:
        carpas debe ser una lista de carpas.

    Postcondiciones:
        Agrega la carpa y devuelve True. Devuelve False si el número no es válido o ya existe.
    """
    if num_carpa <= 0 or _buscar_carpa(carpas, num_carpa) != -1:
        return False
    carpas.append([num_carpa, True])
    return True


def _modificar_carpa(carpas: list, reservas: list, num_actual: int, num_nuevo: int) -> bool:
    """
    Contrato:
        Cambia el número de una carpa y actualiza sus reservas.

    Precondiciones:
        carpas y reservas deben ser listas válidas.

    Postcondiciones:
        Devuelve True si se modificó. Devuelve False si la carpa no existe o el nuevo número
        no es válido o ya está en uso.
    """
    indice = _buscar_carpa(carpas, num_actual)
    if indice == -1 or num_nuevo <= 0 or _buscar_carpa(carpas, num_nuevo) != -1:
        return False

    carpas[indice][CARPA_NUM] = num_nuevo
    for reserva in reservas:
        if reserva[RESERVA_CARPA] == num_actual:
            reserva[RESERVA_CARPA] = num_nuevo
    return True


def _cambiar_estado_carpa(carpas: list, reservas: list, num_carpa: int, activa: bool) -> bool:
    """
    Contrato:
        Activa o inactiva una carpa (borrado lógico).

    Precondiciones:
        carpas y reservas deben ser listas válidas.

    Postcondiciones:
        Devuelve True si se cambió el estado. Devuelve False si la carpa no existe o si se
        intenta inactivar una carpa con reservas registradas.
    """
    indice = _buscar_carpa(carpas, num_carpa)
    if indice == -1:
        return False

    if not activa:
        for reserva in reservas:
            if reserva[RESERVA_CARPA] == num_carpa:
                return False

    carpas[indice][CARPA_ACTIVA] = activa
    return True


def _listar_carpas(carpas: list, solo_activas: bool = False) -> list:
    """
    Contrato:
        Devuelve las carpas ordenadas por número.

    Precondiciones:
        carpas debe ser una lista de carpas.

    Postcondiciones:
        Devuelve una lista nueva ordenada; si solo_activas es True, excluye las inactivas.
    """
    filtradas = [carpa for carpa in carpas if carpa[CARPA_ACTIVA] or not solo_activas]
    return _ordenar(filtradas, lambda carpa: carpa[CARPA_NUM])


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------

def _buscar_cliente(clientes: list, dni: int) -> int:
    """
    Contrato:
        Busca un cliente por DNI.

    Precondiciones:
        clientes debe ser una lista de clientes.

    Postcondiciones:
        Devuelve el índice del cliente o -1 si no existe.
    """
    for indice, cliente in enumerate(clientes):
        if cliente[CLIENTE_DNI] == dni:
            return indice
    return -1


def _registrar_cliente(clientes: list, dni: int, nombre: str, telefono: str) -> bool:
    """
    Contrato:
        Da de alta un cliente con nombre normalizado.

    Precondiciones:
        clientes debe ser una lista de clientes.

    Postcondiciones:
        Agrega el cliente y devuelve True. Devuelve False si el DNI ya existe o algún dato
        no es válido.
    """
    nombre = _normalizar_nombre(nombre)
    if dni <= 0 or nombre == "" or not _validar_telefono(telefono):
        return False
    if _buscar_cliente(clientes, dni) != -1:
        return False
    clientes.append([dni, nombre, telefono.strip()])
    return True


def _buscar_cliente_por_nombre(clientes: list, texto: str) -> list:
    """
    Contrato:
        Busca clientes cuyo nombre contenga el texto, sin distinguir mayúsculas.

    Precondiciones:
        clientes debe ser una lista de clientes.

    Postcondiciones:
        Devuelve una lista con los clientes que coinciden (puede ser vacía).
    """
    texto = texto.strip().lower()
    return [cliente for cliente in clientes if texto in cliente[CLIENTE_NOMBRE].lower()]


def _consultar_reservas_cliente(reservas: list, dni: int) -> list:
    """
    Contrato:
        Devuelve las reservas de un cliente ordenadas por fecha de inicio.

    Precondiciones:
        reservas debe ser una lista de reservas.

    Postcondiciones:
        Devuelve una lista nueva (puede ser vacía).
    """
    propias = [reserva for reserva in reservas if reserva[RESERVA_DNI] == dni]
    return _ordenar(propias, lambda reserva: _fecha_a_clave(reserva[RESERVA_DESDE]))


# ---------------------------------------------------------------------------
# Reservas y alquileres
# ---------------------------------------------------------------------------

def _buscar_reserva(reservas: list, num_carpa: int, dni: int, desde: str) -> int:
    """
    Contrato:
        Busca una reserva por carpa, cliente y fecha de inicio.

    Precondiciones:
        reservas debe ser una lista de reservas.

    Postcondiciones:
        Devuelve el índice de la reserva o -1 si no existe.
    """
    for indice, reserva in enumerate(reservas):
        if (reserva[RESERVA_CARPA] == num_carpa
                and reserva[RESERVA_DNI] == dni
                and _comparar_fechas(reserva[RESERVA_DESDE], desde) == 0):
            return indice
    return -1


def _consultar_estado_carpa(reservas: list, num_carpa: int, desde: str, hasta: str) -> str:
    """
    Contrato:
        Devuelve el estado de una carpa en un rango de fechas.

    Precondiciones:
        Las fechas deben ser válidas y desde <= hasta.

    Postcondiciones:
        Devuelve "libre" si no hay reserva superpuesta; si la hay, devuelve el estado de esa
        reserva ("reservada" o "alquilada").
    """
    for reserva in reservas:
        if (reserva[RESERVA_CARPA] == num_carpa
                and _se_superponen(reserva[RESERVA_DESDE], reserva[RESERVA_HASTA], desde, hasta)):
            return reserva[RESERVA_ESTADO]
    return ESTADO_LIBRE


def _esta_ocupada(reservas: list, num_carpa: int, desde: str, hasta: str) -> bool:
    """
    Contrato:
        Indica si una carpa tiene alguna reserva que se superpone con el rango dado.

    Precondiciones:
        Las fechas deben ser válidas y desde <= hasta.

    Postcondiciones:
        Devuelve True si está ocupada en algún día del rango, False si está libre.
    """
    return _consultar_estado_carpa(reservas, num_carpa, desde, hasta) != ESTADO_LIBRE


def _registrar_reserva(reservas: list, carpas: list, clientes: list, num_carpa: int,
                       dni: int, desde: str, hasta: str,
                       estado: str = ESTADO_RESERVADA) -> bool:
    """
    Contrato:
        Da de alta una reserva o alquiler de una carpa para un cliente en un rango de fechas.

    Precondiciones:
        reservas, carpas y clientes deben ser listas válidas.

    Postcondiciones:
        Agrega la reserva y devuelve True. Devuelve False si la carpa no existe o está
        inactiva, el cliente no existe, las fechas no son válidas, desde > hasta, el estado
        no es válido o la carpa ya está ocupada en ese rango.
    """
    indice_carpa = _buscar_carpa(carpas, num_carpa)
    if indice_carpa == -1 or not carpas[indice_carpa][CARPA_ACTIVA]:
        return False
    if _buscar_cliente(clientes, dni) == -1:
        return False
    if not (_validar_fecha(desde) and _validar_fecha(hasta)):
        return False
    if _comparar_fechas(desde, hasta) > 0:
        return False
    if estado not in (ESTADO_RESERVADA, ESTADO_ALQUILADA):
        return False
    if _esta_ocupada(reservas, num_carpa, desde, hasta):
        return False

    reservas.append([num_carpa, dni, desde, hasta, estado])
    return True


def _cancelar_reserva(reservas: list, num_carpa: int, dni: int, desde: str) -> bool:
    """
    Contrato:
        Da de baja una reserva.

    Precondiciones:
        reservas debe ser una lista de reservas.

    Postcondiciones:
        Elimina la reserva y devuelve True, o devuelve False si no existe.
    """
    indice = _buscar_reserva(reservas, num_carpa, dni, desde)
    if indice == -1:
        return False
    reservas.pop(indice)
    return True


def _cambiar_estado_reserva(reservas: list, num_carpa: int, dni: int, desde: str,
                            estado: str) -> bool:
    """
    Contrato:
        Cambia el estado de una reserva a "reservada" o "alquilada".

    Precondiciones:
        reservas debe ser una lista de reservas.

    Postcondiciones:
        Devuelve True si se modificó. Devuelve False si la reserva no existe o el estado
        no es válido.
    """
    indice = _buscar_reserva(reservas, num_carpa, dni, desde)
    if indice == -1 or estado not in (ESTADO_RESERVADA, ESTADO_ALQUILADA):
        return False
    reservas[indice][RESERVA_ESTADO] = estado
    return True


def _reservas_del_dia(reservas: list, fecha: str) -> list:
    """
    Contrato:
        Devuelve las reservas vigentes en una fecha, ordenadas por número de carpa.

    Precondiciones:
        La fecha debe ser válida.

    Postcondiciones:
        Devuelve una lista nueva (puede ser vacía).
    """
    del_dia = [reserva for reserva in reservas
               if _se_superponen(reserva[RESERVA_DESDE], reserva[RESERVA_HASTA], fecha, fecha)]
    return _ordenar(del_dia, lambda reserva: reserva[RESERVA_CARPA])


def _ordenar_reservas(reservas: list, criterio: str = "fecha") -> list:
    """
    Contrato:
        Ordena las reservas por fecha de inicio o por número de carpa.

    Precondiciones:
        criterio debe ser "fecha" o "carpa".

    Postcondiciones:
        Devuelve una lista nueva ordenada; no modifica la original.
    """
    if criterio == "carpa":
        return _ordenar(reservas, lambda reserva: reserva[RESERVA_CARPA])
    return _ordenar(reservas, lambda reserva: _fecha_a_clave(reserva[RESERVA_DESDE]))


# ---------------------------------------------------------------------------
# Estadísticas
# ---------------------------------------------------------------------------

def _carpas_libres(carpas: list, reservas: list, desde: str, hasta: str) -> list:
    """
    Contrato:
        Devuelve las carpas activas sin reserva en un rango de fechas.

    Precondiciones:
        Las fechas deben ser válidas y desde <= hasta.

    Postcondiciones:
        Devuelve una lista nueva ordenada por número (puede ser vacía).
    """
    activas = _listar_carpas(carpas, solo_activas=True)
    return [carpa for carpa in activas
            if not _esta_ocupada(reservas, carpa[CARPA_NUM], desde, hasta)]


def _calcular_ocupacion(carpas: list, reservas: list, desde: str, hasta: str) -> float:
    """
    Contrato:
        Calcula el porcentaje de carpas activas ocupadas en un rango de fechas.

    Precondiciones:
        Las fechas deben ser válidas y desde <= hasta.

    Postcondiciones:
        Devuelve un valor entre 0 y 100. Si no hay carpas activas devuelve 0.
    """
    activas = _listar_carpas(carpas, solo_activas=True)
    if len(activas) == 0:
        return 0.0
    libres = _carpas_libres(carpas, reservas, desde, hasta)
    ocupadas = len(activas) - len(libres)
    return ocupadas * 100 / len(activas)


def _cliente_con_mas_reservas(reservas: list, clientes: list) -> list | None:
    """
    Contrato:
        Encuentra el cliente con mayor cantidad de reservas.

    Precondiciones:
        reservas y clientes deben ser listas válidas.

    Postcondiciones:
        Devuelve el registro del cliente, o None si no hay reservas.
    """
    mejor_cliente = None
    mejor_cantidad = 0
    for cliente in clientes:
        cantidad = 0
        for reserva in reservas:
            if reserva[RESERVA_DNI] == cliente[CLIENTE_DNI]:
                cantidad += 1
        if cantidad > mejor_cantidad:
            mejor_cantidad = cantidad
            mejor_cliente = cliente
    return mejor_cliente


# ---------------------------------------------------------------------------
# Entrada / salida
# ---------------------------------------------------------------------------

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


def _leer_fecha(mensaje: str) -> str:
    """
    Contrato:
        Solicita una fecha "dd/mm/aaaa" por teclado hasta que sea válida.

    Precondiciones:
        El mensaje debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve una fecha válida.
    """
    while True:
        fecha = input(mensaje).strip()
        if _validar_fecha(fecha):
            return fecha
        print("Error: la fecha debe tener formato dd/mm/aaaa y ser una fecha existente.")


def _leer_rango_fechas() -> list:
    """
    Contrato:
        Solicita dos fechas (desde y hasta) y verifica que desde <= hasta.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Devuelve una lista [desde, hasta] con fechas válidas y ordenadas.
    """
    while True:
        desde = _leer_fecha("Fecha desde (dd/mm/aaaa): ")
        hasta = _leer_fecha("Fecha hasta (dd/mm/aaaa): ")
        if _comparar_fechas(desde, hasta) <= 0:
            return [desde, hasta]
        print("Error: la fecha 'desde' no puede ser posterior a la fecha 'hasta'.")


def _leer_texto(mensaje: str) -> str:
    """
    Contrato:
        Solicita un texto no vacío por teclado.

    Precondiciones:
        El mensaje debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve el texto ingresado sin espacios al inicio ni al final.
    """
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Error: el texto no puede estar vacío.")


def _leer_estado_reserva() -> str:
    """
    Contrato:
        Solicita el estado de una reserva.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Devuelve "reservada" o "alquilada".
    """
    print("  1. Reservada (señada o sin pagar)")
    print("  2. Alquilada (pagada)")
    opcion = _leer_entero("Estado: ", 1)
    while opcion > 2:
        print("Error: opción inválida.")
        opcion = _leer_entero("Estado: ", 1)
    if opcion == 1:
        return ESTADO_RESERVADA
    return ESTADO_ALQUILADA


def _nombre_cliente(clientes: list, dni: int) -> str:
    """
    Contrato:
        Devuelve el nombre de un cliente a partir de su DNI.

    Precondiciones:
        clientes debe ser una lista de clientes.

    Postcondiciones:
        Devuelve el nombre, o "(desconocido)" si el DNI no existe.
    """
    indice = _buscar_cliente(clientes, dni)
    if indice == -1:
        return "(desconocido)"
    return clientes[indice][CLIENTE_NOMBRE]


def _mostrar_carpas(carpas: list) -> None:
    """
    Contrato:
        Muestra una lista de carpas en formato de tabla.

    Precondiciones:
        carpas debe ser una lista de carpas.

    Postcondiciones:
        Imprime la tabla por pantalla o un aviso si la lista está vacía.
    """
    if len(carpas) == 0:
        print("No hay carpas para mostrar.")
        return
    print(f"{'Carpa':>6}  {'Estado':<8}")
    print("-" * 16)
    for carpa in carpas:
        estado = "activa" if carpa[CARPA_ACTIVA] else "inactiva"
        print(f"{carpa[CARPA_NUM]:>6}  {estado:<8}")


def _mostrar_clientes(clientes: list) -> None:
    """
    Contrato:
        Muestra una lista de clientes en formato de tabla.

    Precondiciones:
        clientes debe ser una lista de clientes.

    Postcondiciones:
        Imprime la tabla por pantalla o un aviso si la lista está vacía.
    """
    if len(clientes) == 0:
        print("No hay clientes para mostrar.")
        return
    print(f"{'DNI':>10}  {'Nombre':<25}  {'Teléfono':<15}")
    print("-" * 54)
    for cliente in clientes:
        print(f"{cliente[CLIENTE_DNI]:>10}  {cliente[CLIENTE_NOMBRE]:<25}  "
              f"{cliente[CLIENTE_TELEFONO]:<15}")


def _mostrar_reservas(reservas: list, clientes: list) -> None:
    """
    Contrato:
        Muestra una lista de reservas en formato de tabla, con el nombre del cliente.

    Precondiciones:
        reservas y clientes deben ser listas válidas.

    Postcondiciones:
        Imprime la tabla por pantalla o un aviso si la lista está vacía.
    """
    if len(reservas) == 0:
        print("No hay reservas para mostrar.")
        return
    print(f"{'Carpa':>6}  {'DNI':>10}  {'Cliente':<25}  {'Desde':<10}  {'Hasta':<10}  {'Estado':<9}")
    print("-" * 80)
    for reserva in reservas:
        nombre = _nombre_cliente(clientes, reserva[RESERVA_DNI])
        print(f"{reserva[RESERVA_CARPA]:>6}  {reserva[RESERVA_DNI]:>10}  {nombre:<25}  "
              f"{reserva[RESERVA_DESDE]:<10}  {reserva[RESERVA_HASTA]:<10}  "
              f"{reserva[RESERVA_ESTADO]:<9}")


def _mostrar_resultado(exito: bool, mensaje_ok: str, mensaje_error: str) -> None:
    """
    Contrato:
        Imprime un mensaje según el resultado de una operación.

    Precondiciones:
        Los mensajes deben ser cadenas de caracteres.

    Postcondiciones:
        Imprime mensaje_ok si exito es True, o mensaje_error en caso contrario.
    """
    if exito:
        print(mensaje_ok)
    else:
        print(mensaje_error)


# ---------------------------------------------------------------------------
# Menús
# ---------------------------------------------------------------------------

def _menu_carpas(carpas: list, reservas: list) -> None:
    """
    Contrato:
        Ejecuta el submenú de gestión de carpas.

    Precondiciones:
        carpas y reservas deben ser listas válidas.

    Postcondiciones:
        Modifica carpas según las operaciones elegidas por el usuario.
    """
    while True:
        print("\n--- Carpas ---")
        print("1. Registrar carpa")
        print("2. Listar carpas")
        print("3. Modificar número de carpa")
        print("4. Inactivar carpa")
        print("5. Activar carpa")
        print("6. Consultar estado de una carpa por fechas")
        print("0. Volver")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            numero = _leer_entero("Número de carpa: ", 1)
            _mostrar_resultado(_registrar_carpa(carpas, numero),
                               "Carpa registrada.",
                               "Error: la carpa ya existe.")
        elif opcion == 2:
            _mostrar_carpas(_listar_carpas(carpas))
        elif opcion == 3:
            actual = _leer_entero("Número actual: ", 1)
            nuevo = _leer_entero("Número nuevo: ", 1)
            _mostrar_resultado(_modificar_carpa(carpas, reservas, actual, nuevo),
                               "Carpa modificada.",
                               "Error: la carpa no existe o el nuevo número ya está en uso.")
        elif opcion == 4:
            numero = _leer_entero("Número de carpa: ", 1)
            _mostrar_resultado(_cambiar_estado_carpa(carpas, reservas, numero, False),
                               "Carpa inactivada.",
                               "Error: la carpa no existe o tiene reservas registradas.")
        elif opcion == 5:
            numero = _leer_entero("Número de carpa: ", 1)
            _mostrar_resultado(_cambiar_estado_carpa(carpas, reservas, numero, True),
                               "Carpa activada.",
                               "Error: la carpa no existe.")
        elif opcion == 6:
            numero = _leer_entero("Número de carpa: ", 1)
            if _buscar_carpa(carpas, numero) == -1:
                print("Error: la carpa no existe.")
            else:
                desde, hasta = _leer_rango_fechas()
                estado = _consultar_estado_carpa(reservas, numero, desde, hasta)
                print(f"La carpa {numero} está {estado} entre {desde} y {hasta}.")
        elif opcion == 0:
            return
        else:
            print("Opción inválida.")


def _menu_clientes(clientes: list, reservas: list) -> None:
    """
    Contrato:
        Ejecuta el submenú de gestión de clientes.

    Precondiciones:
        clientes y reservas deben ser listas válidas.

    Postcondiciones:
        Modifica clientes según las operaciones elegidas por el usuario.
    """
    while True:
        print("\n--- Clientes ---")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por nombre")
        print("4. Consultar reservas de un cliente")
        print("0. Volver")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            dni = _leer_entero("DNI: ", 1)
            nombre = _leer_texto("Nombre y apellido: ")
            telefono = _leer_texto("Teléfono: ")
            _mostrar_resultado(_registrar_cliente(clientes, dni, nombre, telefono),
                               "Cliente registrado.",
                               "Error: el DNI ya existe o el teléfono no es válido.")
        elif opcion == 2:
            _mostrar_clientes(_ordenar(clientes, lambda cliente: cliente[CLIENTE_NOMBRE]))
        elif opcion == 3:
            texto = _leer_texto("Texto a buscar: ")
            _mostrar_clientes(_buscar_cliente_por_nombre(clientes, texto))
        elif opcion == 4:
            dni = _leer_entero("DNI: ", 1)
            if _buscar_cliente(clientes, dni) == -1:
                print("Error: el cliente no existe.")
            else:
                _mostrar_reservas(_consultar_reservas_cliente(reservas, dni), clientes)
        elif opcion == 0:
            return
        else:
            print("Opción inválida.")


def _menu_reservas(carpas: list, clientes: list, reservas: list) -> None:
    """
    Contrato:
        Ejecuta el submenú de gestión de reservas y alquileres.

    Precondiciones:
        carpas, clientes y reservas deben ser listas válidas.

    Postcondiciones:
        Modifica reservas según las operaciones elegidas por el usuario.
    """
    while True:
        print("\n--- Reservas y alquileres ---")
        print("1. Registrar reserva / alquiler")
        print("2. Cancelar reserva")
        print("3. Cambiar estado de una reserva")
        print("4. Listar reservas por fecha")
        print("5. Listar reservas por carpa")
        print("6. Reservas del día")
        print("0. Volver")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            numero = _leer_entero("Número de carpa: ", 1)
            dni = _leer_entero("DNI del cliente: ", 1)
            desde, hasta = _leer_rango_fechas()
            estado = _leer_estado_reserva()
            _mostrar_resultado(
                _registrar_reserva(reservas, carpas, clientes, numero, dni, desde, hasta, estado),
                "Reserva registrada.",
                "Error: carpa inexistente o inactiva, cliente inexistente o carpa ocupada en esas fechas.")
        elif opcion == 2:
            numero = _leer_entero("Número de carpa: ", 1)
            dni = _leer_entero("DNI del cliente: ", 1)
            desde = _leer_fecha("Fecha desde de la reserva (dd/mm/aaaa): ")
            _mostrar_resultado(_cancelar_reserva(reservas, numero, dni, desde),
                               "Reserva cancelada.",
                               "Error: la reserva no existe.")
        elif opcion == 3:
            numero = _leer_entero("Número de carpa: ", 1)
            dni = _leer_entero("DNI del cliente: ", 1)
            desde = _leer_fecha("Fecha desde de la reserva (dd/mm/aaaa): ")
            estado = _leer_estado_reserva()
            _mostrar_resultado(_cambiar_estado_reserva(reservas, numero, dni, desde, estado),
                               "Estado actualizado.",
                               "Error: la reserva no existe.")
        elif opcion == 4:
            _mostrar_reservas(_ordenar_reservas(reservas, "fecha"), clientes)
        elif opcion == 5:
            _mostrar_reservas(_ordenar_reservas(reservas, "carpa"), clientes)
        elif opcion == 6:
            fecha = _leer_fecha("Fecha (dd/mm/aaaa): ")
            _mostrar_reservas(_reservas_del_dia(reservas, fecha), clientes)
        elif opcion == 0:
            return
        else:
            print("Opción inválida.")


def _menu_estadisticas(carpas: list, clientes: list, reservas: list) -> None:
    """
    Contrato:
        Ejecuta el submenú de estadísticas.

    Precondiciones:
        carpas, clientes y reservas deben ser listas válidas.

    Postcondiciones:
        Muestra por pantalla la información derivada elegida por el usuario.
    """
    while True:
        print("\n--- Estadísticas ---")
        print("1. Porcentaje de ocupación en un rango de fechas")
        print("2. Carpas libres en un rango de fechas")
        print("3. Cliente con más reservas")
        print("0. Volver")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            desde, hasta = _leer_rango_fechas()
            ocupacion = _calcular_ocupacion(carpas, reservas, desde, hasta)
            print(f"Ocupación entre {desde} y {hasta}: {ocupacion:.1f}%")
        elif opcion == 2:
            desde, hasta = _leer_rango_fechas()
            _mostrar_carpas(_carpas_libres(carpas, reservas, desde, hasta))
        elif opcion == 3:
            cliente = _cliente_con_mas_reservas(reservas, clientes)
            if cliente is None:
                print("No hay reservas registradas.")
            else:
                cantidad = len(_consultar_reservas_cliente(reservas, cliente[CLIENTE_DNI]))
                print(f"{cliente[CLIENTE_NOMBRE]} (DNI {cliente[CLIENTE_DNI]}) "
                      f"con {cantidad} reserva(s).")
        elif opcion == 0:
            return
        else:
            print("Opción inválida.")


def _cargar_datos_iniciales(carpas: list, clientes: list, reservas: list) -> None:
    """
    Contrato:
        Carga datos de ejemplo para probar el sistema.

    Precondiciones:
        Las listas deben estar vacías.

    Postcondiciones:
        Agrega carpas, clientes y reservas de prueba a las listas recibidas.
    """
    for numero in range(1, 11):
        _registrar_carpa(carpas, numero)
    _cambiar_estado_carpa(carpas, reservas, 10, False)

    _registrar_cliente(clientes, 30111222, "juan pérez", "11-5555-1111")
    _registrar_cliente(clientes, 28333444, "MARÍA GÓMEZ", "11 5555 2222")
    _registrar_cliente(clientes, 35555666, "  carlos   lópez ", "+54 11 5555 3333")

    _registrar_reserva(reservas, carpas, clientes, 1, 30111222,
                       "01/01/2027", "15/01/2027", ESTADO_ALQUILADA)
    _registrar_reserva(reservas, carpas, clientes, 2, 28333444,
                       "16/01/2027", "31/01/2027", ESTADO_RESERVADA)
    _registrar_reserva(reservas, carpas, clientes, 3, 30111222,
                       "16/01/2027", "31/01/2027", ESTADO_RESERVADA)
    _registrar_reserva(reservas, carpas, clientes, 1, 35555666,
                       "01/02/2027", "14/02/2027", ESTADO_ALQUILADA)


def main() -> None:
    """
    Contrato:
        Ejecuta el programa principal: carga datos de ejemplo y muestra el menú.

    Precondiciones:
        El archivo debe ejecutarse como programa principal.

    Postcondiciones:
        Permite gestionar carpas, clientes y reservas hasta que el usuario elija salir.
    """
    carpas: list = []
    clientes: list = []
    reservas: list = []
    _cargar_datos_iniciales(carpas, clientes, reservas)

    while True:
        print("\n===== Gestión de carpas del balneario =====")
        print("1. Carpas")
        print("2. Clientes")
        print("3. Reservas y alquileres")
        print("4. Estadísticas")
        print("0. Salir")
        opcion = _leer_entero("Opción: ")

        if opcion == 1:
            _menu_carpas(carpas, reservas)
        elif opcion == 2:
            _menu_clientes(clientes, reservas)
        elif opcion == 3:
            _menu_reservas(carpas, clientes, reservas)
        elif opcion == 4:
            _menu_estadisticas(carpas, clientes, reservas)
        elif opcion == 0:
            print("Hasta luego.")
            return
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
