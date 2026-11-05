# Sombrita - Lectura y escritura de los datos en un archivo JSON.

import json
import os

from src.comunes import (
    ESTADO_ALQUILADA,
    ESTADO_RESERVADA,
    ESTADOS_RESERVA,
    _mostrar_error,
    _validar_fecha,
)


def _cargar_datos_iniciales() -> tuple[dict[int, bool], dict[int, dict], list[dict]]:
    """
    Contrato:
        Genera datos de ejemplo para usar cuando no hay un archivo de
        datos utilizable.

    Precondiciones:
        Ninguna.

    Postcondiciones:
        Devuelve la tupla (carpas, clientes, reservas) según el contrato
        de datos, con reservas sin superposiciones sobre carpas y
        clientes existentes.
    """
    carpas: dict[int, bool] = {numero: True for numero in range(1, 11)}
    carpas[10] = False

    clientes: dict[int, dict] = {
        30111222: {"nombre": "Juan Pérez", "telefono": "11-5555-1111"},
        28333444: {"nombre": "María Gómez", "telefono": "11 5555 2222"},
        35555666: {"nombre": "Carlos López", "telefono": "+54 11 5555 3333"},
    }

    reservas: list[dict] = [
        {
            "carpa": 1,
            "dni": 30111222,
            "desde": "01/01/2027",
            "hasta": "15/01/2027",
            "estado": ESTADO_ALQUILADA,
        },
        {
            "carpa": 2,
            "dni": 28333444,
            "desde": "16/01/2027",
            "hasta": "31/01/2027",
            "estado": ESTADO_RESERVADA,
        },
        {
            "carpa": 3,
            "dni": 30111222,
            "desde": "16/01/2027",
            "hasta": "31/01/2027",
            "estado": ESTADO_RESERVADA,
        },
        {
            "carpa": 1,
            "dni": 35555666,
            "desde": "01/02/2027",
            "hasta": "14/02/2027",
            "estado": ESTADO_ALQUILADA,
        },
    ]
    return (carpas, clientes, reservas)


def _guardar_datos(
    ruta: str, carpas: dict[int, bool], clientes: dict[int, dict], reservas: list[dict]
) -> None:
    """
    Contrato:
        Guarda todas las estructuras en un único archivo JSON.

    Precondiciones:
        Ruta debe ser una cadena de caracteres.
        Las estructuras deben respetar el contrato de datos.

    Postcondiciones:
        Crea la carpeta si no existe y escribe el JSON en UTF-8 con las claves
        "carpas", "clientes" y "reservas".
        Ante un OSError muestra un aviso y no interrumpe el programa.
    """
    contenido = {"carpas": carpas, "clientes": clientes, "reservas": reservas}
    try:
        carpeta = os.path.dirname(ruta)
        if carpeta != "":
            os.makedirs(carpeta, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=4)
    except OSError as error:
        _mostrar_error(f"Aviso: no se pudieron guardar los datos ({error}).")


def _convertir_datos(
    contenido: dict,
) -> tuple[dict[int, bool], dict[int, dict], list[dict]]:
    """
    Contrato:
        Valida lo leído del JSON y lo convierte a las estructuras del
        contrato de datos.

    Precondiciones:
        contenido debe ser el resultado de leer un JSON.

    Postcondiciones:

        Devuelve la tupla (carpas, clientes, reservas), con las claves
        de carpas y clientes
        convertidas a int, porque JSON solo guarda claves de texto.

        Lanza KeyError, ValueError, TypeError o AttributeError si los
        datos no son válidos.
    """
    carpas: dict[int, bool] = {}
    for numero, activa in contenido["carpas"].items():
        if not isinstance(activa, bool):
            raise TypeError(f"la carpa {numero} no tiene un estado booleano")
        carpas[int(numero)] = activa

    clientes: dict[int, dict] = {}
    for dni, datos in contenido["clientes"].items():
        clientes[int(dni)] = {
            "nombre": str(datos["nombre"]),
            "telefono": str(datos["telefono"]),
        }

    reservas: list[dict] = []
    for reserva in contenido["reservas"]:
        carpa, dni = int(reserva["carpa"]), int(reserva["dni"])
        desde, hasta, estado = reserva["desde"], reserva["hasta"], reserva["estado"]

        if carpa not in carpas or dni not in clientes:
            raise ValueError("una reserva apunta a una carpa o un cliente inexistente")

        if not (_validar_fecha(desde) and _validar_fecha(hasta)):
            raise ValueError("una reserva tiene una fecha inválida")

        if estado not in ESTADOS_RESERVA:
            raise ValueError("una reserva tiene un estado inválido")

        reservas.append(
            {
                "carpa": carpa,
                "dni": dni,
                "desde": desde,
                "hasta": hasta,
                "estado": estado,
            }
        )
    return (carpas, clientes, reservas)


def _apartar_archivo_danado(ruta: str) -> str:
    """
    Contrato:
        Renombra un archivo dañado para que el próximo guardado no lo pise.

    Precondiciones:
        Ruta debe ser la ruta de un archivo existente.

    Postcondiciones:
        Devuelve la ruta nueva del archivo, sin sobrescribir respaldos
        anteriores.

        Lanza OSError si no se puede renombrar.
    """
    respaldo = f"{ruta}.corrupto"
    numero = 1
    while os.path.exists(respaldo):
        numero += 1
        respaldo = f"{ruta}.corrupto{numero}"
    os.replace(ruta, respaldo)
    return respaldo


def _cargar_datos(ruta: str) -> tuple[dict[int, bool], dict[int, dict], list[dict]]:
    """
    Contrato:
        Carga las estructuras desde el archivo JSON.

    Precondiciones:
        Ruta debe ser una cadena de caracteres.

    Postcondiciones:
        Devuelve la tupla (carpas, clientes, reservas) según el contrato de datos.
        Si el archivo no existe, devuelve los datos iniciales y los guarda.
        Si el archivo está dañado, muestra un aviso, lo conserva con otro nombre y devuelve
        los datos iniciales.
        Si el archivo no se puede leer, muestra un aviso y devuelve los datos iniciales.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return _convertir_datos(json.load(archivo))
    except FileNotFoundError:
        datos = _cargar_datos_iniciales()
        _guardar_datos(ruta, datos[0], datos[1], datos[2])
        return datos
    except (
        json.JSONDecodeError,
        KeyError,
        ValueError,
        TypeError,
        AttributeError,
    ) as error:
        _mostrar_error(f"Aviso: el archivo de datos está dañado ({error}).")
        try:
            respaldo = _apartar_archivo_danado(ruta)
            _mostrar_error(
                f"Se conservó una copia en {respaldo}. Se usan datos de ejemplo."
            )
        except OSError as error_respaldo:
            _mostrar_error(f"Aviso: no se pudo apartar el archivo ({error_respaldo}).")
        return _cargar_datos_iniciales()
    except OSError as error:
        _mostrar_error(
            f"Aviso: no se pudo leer el archivo ({error}). Se usan datos de ejemplo."
        )
        return _cargar_datos_iniciales()
