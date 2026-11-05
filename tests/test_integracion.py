# Pruebas del programa completo: simulan lo que un usuario escribe por teclado.
# Comprueban que main.py, los menús y la persistencia funcionan juntos.

import json

import pytest

import main as programa
from src.persistencia import _cargar_datos


@pytest.fixture
def ruta_datos(tmp_path, monkeypatch) -> str:
    """Hace que el programa use un archivo temporal en lugar de datos/sombrita.json."""
    ruta = str(tmp_path / "sombrita.json")
    monkeypatch.setattr(programa, "ARCHIVO_DATOS", ruta)
    return ruta


def _leer_json(ruta: str) -> dict:
    """Lee el archivo de datos tal como quedó en el disco."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def test_salir_directo(ruta_datos, simular_teclado, capsys):
    """Abrir y salir: crea el archivo con los datos de ejemplo."""
    simular_teclado(["0"])
    programa.main()
    assert "Hasta luego." in capsys.readouterr().out
    assert len(_leer_json(ruta_datos)["carpas"]) == 10


def test_opciones_invalidas_no_rompen(ruta_datos, simular_teclado, capsys):
    """Opciones inexistentes y texto en cada menú: avisa y sigue."""
    simular_teclado(["9", "abc", "1", "9", "0", "2", "9", "0", "3", "9", "0", "0"])
    programa.main()
    assert capsys.readouterr().out.count("Opción inválida.") == 4


def test_registrar_carpa_persiste_sin_salir(ruta_datos, simular_teclado):
    """Guarda después de cada cambio: si se corta antes de salir, el dato ya está en disco."""
    simular_teclado(["1", "1", "50"])
    with pytest.raises(StopIteration):
        programa.main()
    assert _leer_json(ruta_datos)["carpas"]["50"] is True


def test_datos_siguen_al_reabrir(ruta_datos, simular_teclado):
    """Cerrar y volver a abrir: los datos siguen ahí."""
    simular_teclado(["1", "1", "50", "0", "0"])
    programa.main()
    simular_teclado(["0"])
    programa.main()
    assert _cargar_datos(ruta_datos)[0][50] is True


def test_reserva_con_cliente_nuevo(ruta_datos, simular_teclado, capsys):
    """DNI desconocido: pide los datos del cliente, y registra cliente y reserva."""
    simular_teclado(["2", "1", "5", "40000000", "ana ruiz", "11-5555-9999",
                     "01/03/2027", "05/03/2027", "2", "0", "0"])
    programa.main()
    assert "Reserva registrada." in capsys.readouterr().out
    _, clientes, reservas = _cargar_datos(ruta_datos)
    assert clientes[40000000]["nombre"] == "Ana Ruiz"
    assert reservas[-1] == {"carpa": 5, "dni": 40000000, "desde": "01/03/2027",
                            "hasta": "05/03/2027", "estado": "alquilada"}


def test_reserva_con_cliente_existente_no_pide_datos(ruta_datos, simular_teclado):
    """DNI conocido: pasa directo a las fechas."""
    simular_teclado(["2", "1", "5", "30111222", "01/03/2027", "05/03/2027", "1", "0", "0"])
    programa.main()
    assert _cargar_datos(ruta_datos)[2][-1]["dni"] == 30111222


def test_reserva_telefono_invalido_no_registra_nada(ruta_datos, simular_teclado, capsys):
    """Teléfono inválido: avisa y no pide fechas ni agrega datos."""
    simular_teclado(["2", "1", "5", "40000000", "Ana", "sin teléfono", "0", "0"])
    programa.main()
    assert "el teléfono no es válido" in capsys.readouterr().out
    assert 40000000 not in _cargar_datos(ruta_datos)[1]


def test_cliente_nuevo_se_guarda_aunque_falle_la_reserva(ruta_datos, simular_teclado):
    """El cliente ya quedó registrado: se guarda en el momento, aunque la carpa no exista."""
    simular_teclado(["2", "1", "99", "40000000", "Ana", "11-5555-9999",
                     "01/03/2027", "05/03/2027", "1"])
    with pytest.raises(StopIteration):
        programa.main()
    assert "40000000" in _leer_json(ruta_datos)["clientes"]


def test_reserva_carpa_ocupada_rechazada(ruta_datos, simular_teclado, capsys):
    """La carpa 1 ya está alquilada del 01/01 al 15/01/2027 en los datos de ejemplo."""
    simular_teclado(["2", "1", "1", "28333444", "10/01/2027", "12/01/2027", "1", "0", "0"])
    programa.main()
    assert "Error: la carpa no existe, está inactiva o está ocupada" in capsys.readouterr().out
    assert len(_cargar_datos(ruta_datos)[2]) == 4


def test_cancelar_y_cambiar_estado(ruta_datos, simular_teclado):
    """Cambia el estado de una reserva, cancela otra y lo guarda."""
    simular_teclado(["2",
                     "3", "2", "28333444", "16/01/2027", "2",
                     "2", "3", "30111222", "16/01/2027",
                     "0", "0"])
    programa.main()
    reservas = _cargar_datos(ruta_datos)[2]
    assert len(reservas) == 3
    assert [r["estado"] for r in reservas if r["carpa"] == 2] == ["alquilada"]


def test_listados_de_reservas(ruta_datos, simular_teclado, capsys):
    """Cada opción de listado muestra los resultados, y avisa si no hay."""
    simular_teclado(["2", "4", "5", "6", "juan", "7", "2", "01/02/2027", "7", "2", "01/06/2027",
                     "0", "0"])
    programa.main()
    salida = capsys.readouterr().out
    assert "Juan Pérez" in salida and "Carlos López" in salida
    assert "No hay reservas para mostrar." in salida


def test_menu_carpas_completo(ruta_datos, simular_teclado, capsys):
    """Recorre las opciones de carpas: listar, modificar, inactivar, activar y consultar."""
    simular_teclado(["1",
                     "2",
                     "3", "9", "90",
                     "4", "2", "90",
                     "4", "1", "90",
                     "4", "3",
                     "5", "1", "05/01/2027", "06/01/2027",
                     "5", "99",
                     "0", "0"])
    programa.main()
    salida = capsys.readouterr().out
    assert "Carpa modificada." in salida
    assert "Carpa inactivada." in salida
    assert "Carpa activada." in salida
    assert "La carpa 1 está alquilada entre 05/01/2027 y 06/01/2027." in salida
    assert "Error: la carpa no existe." in salida
    assert _cargar_datos(ruta_datos)[0][90] is True


def test_menu_estadisticas_completo(ruta_datos, simular_teclado, capsys):
    """Datos de ejemplo: 9 carpas activas y 2 ocupadas (la 2 y la 3) del 16 al 31/01/2027."""
    simular_teclado(["3",
                     "1", "16/01/2027", "31/01/2027",
                     "2", "16/01/2027", "31/01/2027",
                     "3",
                     "0", "0"])
    programa.main()
    salida = capsys.readouterr().out
    assert "22.2%" in salida
    assert "Carpa libre" in salida
    assert "Juan Pérez (DNI 30111222) con 2 reserva(s)." in salida


def test_ctrl_c_guarda_y_sale(ruta_datos, monkeypatch, capsys):
    """Ctrl+C durante el menú: no muestra un error de Python, guarda y sale prolijo."""
    def _interrumpir(mensaje: str = "") -> str:
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", _interrumpir)
    programa.main()
    assert "Hasta luego." in capsys.readouterr().out
    assert len(_leer_json(ruta_datos)["reservas"]) == 4


def test_archivo_danado_no_impide_arrancar(ruta_datos, simular_teclado, capsys):
    """Con el archivo roto, el programa arranca, guarda y conserva la copia dañada."""
    with open(ruta_datos, "w", encoding="utf-8") as archivo:
        archivo.write("roto")
    simular_teclado(["0"])
    programa.main()
    assert "dañado" in capsys.readouterr().out
    with open(ruta_datos + ".corrupto", encoding="utf-8") as archivo:
        assert archivo.read() == "roto"
