# datos/

Acá vive `sombrita.json`, el único archivo de datos del programa. Lo crea y lo actualiza el programa.
Git lo ignora, así que cada integrante tiene su propia copia.

## Formato

```json
{
    "carpas": {"1": true, "10": false},
    "clientes": {"30111222": {"nombre": "Juan Pérez", "telefono": "11-5555-1111"}},
    "reservas": [
        {"carpa": 1, "dni": 30111222, "desde": "01/01/2027", "hasta": "15/01/2027",
         "estado": "alquilada"}
    ]
}
```

JSON guarda las claves como texto. `_convertir_datos` las vuelve a pasar a `int` al cargar.

## Cuándo se lee y se escribe

- **Lectura:** una vez, al abrir el programa.
- **Escritura:** después de cada cambio exitoso, al salir y al interrumpir con Ctrl+C.

## Qué pasa si hay un problema

| Situación | Qué hace el programa |
|---|---|
| El archivo no existe | Usa datos de ejemplo y crea el archivo. |
| JSON roto o datos inválidos | Avisa, lo renombra a `sombrita.json.corrupto` y usa datos de ejemplo. |
| Ya existe un `.corrupto` | Usa `.corrupto2`, `.corrupto3`, etc., sin pisar los anteriores. |
| No se puede leer el archivo | Avisa y usa datos de ejemplo. |
| No se puede escribir | Avisa y el programa sigue, pero ese cambio no queda guardado. |

Se considera dañado un archivo con campos faltantes, carpas no booleanas, fechas o estados inválidos, o reservas que apuntan a una carpa o un cliente inexistente.

Para volver a los datos de ejemplo, cerrá el programa y borrá `sombrita.json`.
