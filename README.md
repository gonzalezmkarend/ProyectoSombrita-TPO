# Sombrita

Sistema de gestión de carpas para un balneario.

Trabajo Práctico Obligatorio de  Algoritmos y Estructuras de Datos I (UADE).

## Funcionalidades

| Menú | Operaciones |
|---|---|
| Carpas | Registrar, listar, cambiar el número, activar o inactivar, y consultar el estado por fechas. |
| Reservas y alquileres | Registrar con alta de cliente, cancelar, cambiar el estado, listar, buscar por cliente y ver las reservas del día (hoy u otra fecha). |
| Estadísticas | Porcentaje de ocupación, carpas libres y cliente con más reservas. |

Una **reserva** está señada o sin pagar; un **alquiler** está pagado. La gestión de cobros queda fuera del alcance.

## Requisitos

- Python 3.10 o superior.
- Dependencias: `tabulate`, `colorama` y `pytest`, listadas en `requirements.txt`.

## Instalación y uso

Los comandos se ejecutan desde la raíz del repositorio.

```bash
python -m pip install -r requirements.txt
python main.py
```

La primera ejecución crea `datos/sombrita.json` con datos de ejemplo.

## Pruebas

```bash
python -m pytest
```

El detalle de la cobertura está en [`tests/README.md`](tests/README.md).

## Estructura del repositorio

```text
.
├── main.py                     Punto de entrada: carga los datos e integra los menús
├── requirements.txt            Dependencias
├── pytest.ini                  Configuración de pytest
├── src/                        Código del programa
│   ├── comunes.py              Constantes, fechas, ordenamiento, pantalla y teclado
│   ├── persistencia.py         Lectura y escritura del archivo JSON
│   ├── menu_carpas.py          Lógica y submenú de carpas
│   ├── menu_reservas.py        Lógica y submenú de clientes, reservas y alquileres
│   └── menu_estadisticas.py    Lógica y submenú de estadísticas
├── tests/                      Pruebas automatizadas
├── datos/                      Archivo de datos del programa
├── docs/                       Consigna y presentación
└── etapa1/                     Código de la Entrega 1
```

Cada carpeta tiene su propio README: [`src/`](src/README.md), [`tests/`](tests/README.md), [`datos/`](datos/README.md), [`docs/`](docs/README.md) y [`etapa1/`](etapa1/README.md).

## Arquitectura

Las dependencias entre módulos van en un solo sentido:

```text
                         main.py
           ┌────────────────┼───────────────────┐
           v                v                   v
     menu_carpas      menu_reservas     menu_estadisticas
           │                │                   │
           v                v                   │
              persistencia                      │
                    │                           │
                    v                           v
                         comunes
```

`main.py` también usa directamente `persistencia` y `comunes`.

Flujo de una operación:

1. `main()` carga `carpas`, `clientes` y `reservas`, y los pasa por parámetro al menú elegido.
2. El menú lee los datos del usuario y llama a una función de lógica, que no usa `input()` ni `print()`.
3. El menú muestra el resultado y, si hubo cambios, guarda el archivo.
4. Al salir o al interrumpir con Ctrl+C, `main()` guarda los datos y termina.

## Modelo de datos

```python
# Número de carpa -> activa
carpas: dict[int, bool] = {1: True, 10: False}

# DNI -> datos del cliente
clientes: dict[int, dict] = {
    30111222: {"nombre": "Juan Pérez", "telefono": "11-5555-1111"},
}

# Una carpa puede tener varias reservas, en fechas distintas
reservas: list[dict] = [
    {"carpa": 1, "dni": 30111222, "desde": "01/01/2027", "hasta": "15/01/2027",
     "estado": "alquilada"},
]

ESTADOS_RESERVA: tuple[str, str] = ("reservada", "alquilada")
```

Las fechas se almacenan como texto `"dd/mm/aaaa"` y se convierten a `datetime` para validarlas y compararlas. Los conjuntos (`set`) se usan para carpas ocupadas y DNI distintos. El ordenamiento usa quicksort recursivo.

## Reglas de negocio

- El número de carpa y el DNI son mayores a 0 y únicos.
- Las carpas no se eliminan: se inactivan (borrado lógico).
- Una carpa con reservas registradas no se puede inactivar.
- Una reserva requiere una carpa activa, un cliente existente, fechas válidas con `desde <= hasta` y un estado válido.
- Dos reservas de una misma carpa no pueden compartir ningún día.
- Una reserva se identifica por carpa, DNI y fecha de inicio.
- Un cliente nuevo se conserva aunque la reserva que se estaba cargando sea rechazada.

## Convenciones de código

- Funciones con prefijo `_`, salvo `main()` y las pruebas `test_...`.
- Docstring con Contrato, Precondiciones y Postcondiciones, y type hints en las funciones del programa.
- Sin clases ni variables globales; solo constantes en mayúsculas.
