# Pruebas de src/persistencia.py.
# tmp_path es una carpeta temporal que da pytest: las pruebas nunca tocan datos/sombrita.json.

import json

import pytest

from src.comunes import ESTADOS_RESERVA, _se_superponen, _validar_fecha
from src.persistencia import _cargar_datos, _cargar_datos_iniciales, _guardar_datos


def _escribir(ruta, texto: str) -> None:
    """Crea un archivo de prueba con el texto indicado."""
    ruta.write_text(texto, encoding="utf-8")


def test_guardar_y_cargar_devuelve_lo_mismo(tmp_path, carpas, clientes, reservas):
    """Persistencia: lo cargado es igual a lo guardado, con las claves como int."""
    ruta = str(tmp_path / "datos.json")
    _guardar_datos(ruta, carpas, clientes, reservas)
    assert _cargar_datos(ruta) == (carpas, clientes, reservas)


def test_cargar_convierte_claves_a_int(tmp_path, carpas, clientes, reservas):
    """JSON guarda las claves como texto: al cargar tienen que volver a ser int."""
    ruta = str(tmp_path / "datos.json")
    _guardar_datos(ruta, carpas, clientes, reservas)
    carpas_leidas, clientes_leidos, _ = _cargar_datos(ruta)
    assert all(isinstance(clave, int) for clave in carpas_leidas)
    assert all(isinstance(clave, int) for clave in clientes_leidos)


def test_guardar_conserva_tildes(tmp_path, carpas, clientes, reservas):
    """ensure_ascii=False: el archivo es legible, con "Pérez" y no con "P\\u00e9rez"."""
    ruta = tmp_path / "datos.json"
    _guardar_datos(str(ruta), carpas, clientes, reservas)
    assert "Juan Pérez" in ruta.read_text(encoding="utf-8")


def test_guardar_crea_la_carpeta(tmp_path, carpas, clientes, reservas):
    """Si la carpeta no existe, se crea."""
    ruta = tmp_path / "nueva" / "carpeta" / "datos.json"
    _guardar_datos(str(ruta), carpas, clientes, reservas)
    assert ruta.exists()


def test_guardar_sin_poder_escribir_no_falla(tmp_path, carpas, clientes, reservas, capsys):
    """Error de archivo: la ruta es una carpeta. Avisa y el programa sigue."""
    _guardar_datos(str(tmp_path), carpas, clientes, reservas)
    assert "no se pudieron guardar" in capsys.readouterr().out


def test_cargar_archivo_inexistente(tmp_path):
    """Error de archivo: usa los datos iniciales y crea el archivo."""
    ruta = tmp_path / "datos.json"
    assert _cargar_datos(str(ruta)) == _cargar_datos_iniciales()
    assert ruta.exists()


def test_cargar_json_corrupto_conserva_el_archivo(tmp_path, capsys):
    """Error de archivo: no se cae, avisa y conserva una copia con el contenido original."""
    ruta = tmp_path / "datos.json"
    _escribir(ruta, "{esto no es json")
    assert _cargar_datos(str(ruta)) == _cargar_datos_iniciales()
    assert "dañado" in capsys.readouterr().out
    assert (tmp_path / "datos.json.corrupto").read_text(encoding="utf-8") == "{esto no es json"
    assert not ruta.exists()


def test_cargar_corrupto_no_pisa_respaldos_anteriores(tmp_path):
    """Dos archivos dañados seguidos generan dos copias distintas."""
    ruta = tmp_path / "datos.json"
    _escribir(ruta, "primero")
    _cargar_datos(str(ruta))
    _escribir(ruta, "segundo")
    _cargar_datos(str(ruta))
    assert (tmp_path / "datos.json.corrupto").read_text(encoding="utf-8") == "primero"
    assert (tmp_path / "datos.json.corrupto2").read_text(encoding="utf-8") == "segundo"


def test_guardar_despues_de_corrupto_no_pisa_la_copia(tmp_path):
    """El guardado que sigue al arranque no destruye el archivo dañado."""
    ruta = tmp_path / "datos.json"
    _escribir(ruta, "dañado")
    datos = _cargar_datos(str(ruta))
    _guardar_datos(str(ruta), datos[0], datos[1], datos[2])
    assert (tmp_path / "datos.json.corrupto").read_text(encoding="utf-8") == "dañado"


CLIENTE_OK = {"nombre": "Ana", "telefono": "11-5555-3333"}
RESERVA_OK = {"carpa": 1, "dni": 1, "desde": "01/01/2027", "hasta": "02/01/2027",
              "estado": "reservada"}


@pytest.mark.parametrize("contenido", [
    [],                                                                   # no es un objeto
    {"carpas": {}, "clientes": {}},                                       # falta "reservas"
    {"carpas": {"uno": True}, "clientes": {}, "reservas": []},            # número no entero
    {"carpas": {"1": "si"}, "clientes": {}, "reservas": []},              # estado no booleano
    {"carpas": {}, "clientes": {"1": {"nombre": "Ana"}}, "reservas": []},  # falta teléfono
    {"carpas": {}, "clientes": {"1": CLIENTE_OK}, "reservas": [RESERVA_OK]},   # carpa inexistente
    {"carpas": {"1": True}, "clientes": {}, "reservas": [RESERVA_OK]},    # cliente inexistente
    {"carpas": {"1": True}, "clientes": {"1": CLIENTE_OK},
     "reservas": [{**RESERVA_OK, "desde": "31/04/2027"}]},                # fecha inválida
    {"carpas": {"1": True}, "clientes": {"1": CLIENTE_OK},
     "reservas": [{**RESERVA_OK, "estado": "pagada"}]},                   # estado inválido
])
def test_cargar_contenido_invalido(tmp_path, capsys, contenido):
    """JSON bien formado con datos inválidos: se trata como archivo dañado."""
    ruta = tmp_path / "datos.json"
    _escribir(ruta, json.dumps(contenido))
    assert _cargar_datos(str(ruta)) == _cargar_datos_iniciales()
    assert "dañado" in capsys.readouterr().out


def test_datos_iniciales_respetan_las_reglas():
    """Los datos de ejemplo cumplen las reglas que el programa exige a cualquier reserva."""
    carpas, clientes, reservas = _cargar_datos_iniciales()
    for reserva in reservas:
        assert carpas[reserva["carpa"]] is True
        assert reserva["dni"] in clientes
        assert _validar_fecha(reserva["desde"]) and _validar_fecha(reserva["hasta"])
        assert reserva["estado"] in ESTADOS_RESERVA
    for indice, reserva in enumerate(reservas):
        for otra in reservas[indice + 1:]:
            if reserva["carpa"] == otra["carpa"]:
                assert not _se_superponen(reserva["desde"], reserva["hasta"],
                                          otra["desde"], otra["hasta"])
